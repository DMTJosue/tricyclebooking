import contextlib
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseNotFound
# to activate the user accounts
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
# getting token from utils.py
from .utils import TokenGenerator,generate_token

# emails
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.conf import settings
#from resend import Resend 

#resetpassword generators
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# threading
import threading

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        
        self.email_message = email_message
        threading.Thread.__init__(self)
       
    def run(self):
        self.email_message.send()

# Create your views here.
def signup(request):
    if request.method != "POST":
        return render(request,'auth/signup.html')
    username=request.POST['email']
    first_name=request.POST['fname']
    last_name=request.POST['lname']
    email=request.POST['email']
    password=request.POST['pass1']
    confirm_password=request.POST['pass2']
    if password!=confirm_password:
        messages.warning(request,"Les mots de passes ne correspondent pas")
        return render(request,'auth/signup.html')


    with contextlib.suppress(Exception):
        if User.objects.get(username=email):

            messages.warning(request,"L'email est déjà utilisé")
            return render(request,'auth/signup.html')


    user = User.objects.create_user(username,email,password)
    user.is_active=False
    user.first_name=first_name
    user.last_name=last_name
    user.save()
    current_site = get_current_site(request)
    email_subject = "Activer votre compte"
    message = render_to_string('auth/activate.html',{
        'user': user,
        'domain': settings.DOMAIN,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })



    email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
    EmailThread(email_message).start()

    messages.info(request,"Activer votre compte en cliquant sur le lien dans votre email")
    return redirect('Tricycleauth:handlelogin')

class ActivateAccountView(View):

    def get(self, request, uidb64, token):

        try:
            uid = str(urlsafe_base64_decode(uidb64), 'utf-8')  
        except ValueError:
            return render(request, 'activatefail.html')

        user = get_object_or_404(User, pk=uid)

        if generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Compte activé avec succès")
            return redirect(reverse('Tricycleauth:handlelogin'))
        else: 
            return HttpResponseNotFound()
        
    
def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Connexion réussie")
            return render(request,'Tricycle/index.html')

        else:
            messages.error(request,"Identifiants invalides")
            return redirect('Tricycleauth:handlelogin')

    return render(request,'auth/login.html')  


def handlelogout(request):
    logout(request)
    messages.success(request,"Déconnexion réussie")
    return redirect('Tricycleauth:handlelogin')
         

class RequestResetEmailView(View):
    
    def get(self, request):
        return render(request,'auth/request-reset-email.html' )
    
    def post(self,request):
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if user.exists():

            self._extracted_from_post_6(user, email, request)
        else:
            messages.error(request, "Vous n'êtes pas un utilisateur , inscrivez-vous")

        return render(request,'auth/request-reset-email.html')

    # TODO Rename this here and in `post`
    def _extracted_from_post_6(self, user, email, request):
        email_subject = '[Réinitialiser votre mot de passe]'
        token_generator = PasswordResetTokenGenerator()

        message = render_to_string('auth/reset-user-password.html', {
            'domain': settings.DOMAIN, 
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': token_generator.make_token(user[0])
        })

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )

        EmailThread(email_message).start()

        messages.info(request,'Nous vous avons un email, suivez les instructions pour réinitialiser votre mot de passe')
        
class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        with contextlib.suppress(DjangoUnicodeDecodeError):
            user_id = str(urlsafe_base64_decode(uidb64), 'utf-8')
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Le lien de réinitialisation du mot de passe est invalide")
                return render(request,'aut/request-reset-email.html')

        return render(request,'auth/set-new-password.html',context)
    
    def post(self, request, uidb64,token):
        context ={
            'uidb64': uidb64,
            'token': token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Les mots de passes ne correspondent pas")
            return render(request,'auth/set-new-password.html',context)

        try:
            return self._extracted_from_post_13(uidb64, password, request)
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Quelque chose s'est mal passée")
            return render(request,'auth/set-new-password.html',context)

        return render(request,'auth/set-new-password.html',context)

    # TODO Rename this here and in `post`
    def _extracted_from_post_13(self, uidb64, password, request):
        user_id = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = User.objects.get(pk=user_id)
        user.set_password(password)
        user.save()
        messages.success(request,"Mot de passe réinitialiser avec succès veuillez vous connecter avec le nouveau mot de passe")
        return redirect('Tricycleauth:handlelogin')
        