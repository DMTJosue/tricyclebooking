from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Modele, Tricycle
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import TricycleForm ,ReservationForm,ContactForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView,DeleteView
from .models import Reservation
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.db import IntegrityError
# Create your views here.
from django.core.mail import send_mail
from django.conf import settings



def index(request):
    return render(request,'index.html')
class TricycleView(ListView):
    template_name='Tricycle/index.html'
    modeles = Modele.objects.all()
    tricycles = Tricycle.objects.all()[:3]

    def get(self, request):
        return render(request, self.template_name, {'tricycles': self.tricycles, 'modeles': self.modeles,})


class TricycleList(ListView):
    template_name = 'Tricycle/list.html'
    tricycles = Tricycle.objects.all()
    modeles = Modele.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'modeles': self.modeles, 'tricycles': self.tricycles})


class TricycleDetail(DetailView):
    template_name = 'Tricycle/detail.html'
    modeles = Modele.objects.all()

    def get(self, request, *args, **kwargs):
        tricycle = Tricycle.objects.get(pk=self.kwargs['pk'])
        return render(request, self.template_name, {'modeles': self.modeles, 'tricycle': tricycle})
        

class TricycleAdd(PermissionRequiredMixin, CreateView):	
    permission_required = 'tricycle.add_tricycle'	
    model = Tricycle
    template_name = 'Tricycle/add.html'
    form_class = TricycleForm
    success_url = reverse_lazy('tricycle:list')


class TricycleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'tricycle.change_tricycle'		
    model = Tricycle
    template_name = 'Tricycle/update.html'
    form_class = TricycleForm
    success_url = reverse_lazy('tricycle:list')


class TricycleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'tricycle.delete_tricycle'		
    model = Tricycle
    success_url = reverse_lazy('tricycle:list')


class TricycleAchat(LoginRequiredMixin, View):
    login_required = True
    template_name = 'Tricycle/payement.html'
    modeles = Modele.objects.all()

    def get(self, request, *args, **kwargs):
        tricycle = Tricycle.objects.get(pk=self.kwargs['pk'])
        current_date = timezone.now().date()
        context = {
            'current_date': current_date,
            'tricycle': tricycle,
            'modeles': self.modeles,
            'form': TricycleForm(initial={'start_date': current_date}),  # Ajout de la date actuelle dans le formulaire
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = TricycleForm(request.POST)
        tricycle = Tricycle.objects.get(pk=self.kwargs['pk'])

        if form.is_valid():
            tricycle = form.save(commit=False)
            tricycle.save()
            nouveau_prix = tricycle.calculate_new_price()
            return render(request, self.template_name, {'form': form, 'tricycle': tricycle, 'nouveau_prix': nouveau_prix})

        return render(request, self.template_name, {'form': form, 'tricycle': tricycle})



class ReservationView(LoginRequiredMixin, View):
    template_name = 'Tricycle/success.html'
    form_class = ReservationForm
    error_template_name = 'Tricycle/error.html'
    
    def get(self, request, tricycle_id):
        form = self.form_class()
        tricycle = Tricycle.objects.get(id=tricycle_id)
        return render(request, 'reservation.html', {'form': form, 'tricycle': tricycle})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            modele = user_data['modele']
            adress = user_data['adress']
            name = user_data['name']
            #price = user_data['price'].replace(',', '.')
            start_date = user_data['start_date']
            end_date = user_data['end_date']
            heure_debut = user_data['heure_debut']
            heure_fin = user_data['heure_fin']
            tranche = user_data['tranche']
            nouveau_prix = user_data['nouveau_prix']
            apayer = user_data['apayer']
            phone = user_data['phone']
            montant_restant = user_data['montant_restant']
            
            # Récupérer le nom et prénom de l'utilisateur
            first_name = self.request.user.first_name
            last_name = self.request.user.last_name
            email=self.request.user.email
            
            try:
                # Créer une instance du modèle Reservation et enregistrer les données
                reservation = Reservation( 
                    first_name=first_name,
                    last_name=last_name,
                    modele=modele,
                    adress=adress,
                    name=name,
                    #price=price,
                    start_date=start_date,
                    end_date=end_date,
                    heure_debut=heure_debut,
                    heure_fin=heure_fin,
                    tranche=tranche,
                    email=email,
                    nouveau_prix=nouveau_prix,
                    apayer=apayer,
                    montant_restant=montant_restant,
                    phone = phone
                )
                
                reservation.save()
                
                if 'payer' in request.POST:
                    # Mettre à jour le champ payé
                    reservation.paye = True
                    reservation.save()
                    
                print("La réservation a été enregistrée avec succès.")
            except IntegrityError as e:
                print(f"Erreur lors de l'enregistrement de la réservation : {e}")
            
            return render(request, self.template_name, {'reservation': reservation})  # Redirige vers la page de succès
        return render(request, self.error_template_name, {'form': form})

def contact(request):
    
    def send_email( email, subject, full_message):

        send_mail(
            subject,
            full_message,
            email,
            [settings.EMAIL_HOST_USER] 
        )

    def handle_form(form):

        name = form.cleaned_data['name']  
        email = form.cleaned_data['email']  
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        full_message = f"Nom : {name}\n\nEmail : {email}\n\nMessage :{message}"

        try:
            send_email(email,subject,full_message)
        
        except Exception as e:
        
            return render(request, 'Tricycle/contact.html', {'form': form})

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            handle_form(form)


    else:
        form = ContactForm()

    return render(request, 'Tricycle/contact.html', {'form': form})

def payement_view(request):
    if request.method == 'POST':
      reservation_id = request.POST['reservation_id']
      reservation = Reservation.objects.get(id=reservation_id)

     # Mettre à jour les champs de la réservation
      reservation.paye=1

      reservation.save()

      return render(request, 'Tricycle/confirmation.html')
    else:
        # Afficher le formulaire initialement
        reservation = Reservation.objects.get(id=1)
        return render(request, 'form.html', {'reservation': reservation})
    
def confirmation_view(request):
  return render(request, 'success.html')





