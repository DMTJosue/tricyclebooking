from django import forms
from .models import Modele, Tricycle ,Reservation



class TricycleForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Tricycle
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'lorem ipsum',
            }),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '123457.90',
                }
            ),

            'modele': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class ReservationForm(forms.Form):
    adress=forms.CharField( required=True)
    name = forms.CharField()
    modele = forms.CharField()
    #price = forms.DecimalField(max_digits=10,decimal_places=2)
    #price = forms.DecimalField(required=False,max_digits=10, decimal_places=2)

    phone = forms.CharField() # Ajout du champ phone
    nouveau_prix = forms.DecimalField(max_digits=10, decimal_places=2)
    montant_restant = forms.DecimalField(max_digits=10, decimal_places=2)
    start_date = forms.DateField()
    end_date = forms.DateField()
    heure_debut = forms.TimeField()
    heure_fin = forms.TimeField()
    apayer=forms.DecimalField()
    tranche = forms.CharField()

class ContactForm(forms.Form):

  name = forms.CharField(label='Nom', max_length=100)
  email = forms.EmailField(
  required=True,
  error_messages={
    'required': "Veuillez entrer votre email"
  })

  subject = forms.CharField(max_length=100)
  message = forms.CharField(max_length=255)

  

    