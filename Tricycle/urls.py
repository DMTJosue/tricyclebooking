"""
URL configuration for Tricycle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns

from Tricycleapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TricycleView.as_view(), name='index'),
    path('Tricycle',include('Tricycleapp.urls')),
    path('Tricycleauth/',include('Tricycleauth.urls')),
    path('Modele/', include('Modele.urls', namespace='Modele')),
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', views.TricycleView.as_view(), name='index'),
    path('Tricycle/',include('Tricycleapp.urls',namespace='tricycle')),
    path('Tricycleauth/',include('Tricycleauth.urls',namespace='tricycleauth')), 
    path('Modele/', include('Modele.urls', namespace='modele')),
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



'''
On utilise souvent un nom pour les apps quand on écrit plusieurs applications
et dont les noms des urls spnt les memes. Alors les app_namme permettent de se
rediriger vers cet url selin de nom de l'app defini
'''