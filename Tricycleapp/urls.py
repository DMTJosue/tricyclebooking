from django.urls import path
from Tricycleapp import views


app_name = 'Tricycleapp'

urlpatterns = [
    path('<int:pk>/', views.TricycleDetail.as_view(), name='detail'),
	path('list/', views.TricycleList.as_view(), name='list'),
	path('add/', views.TricycleAdd.as_view(), name='add'),
	path('update/<int:pk>/', views.TricycleUpdate.as_view(), name='update'),
	path('delete/<int:pk>/', views.TricycleDelete.as_view(), name="delete"),
	path('<int:pk>/achat/', views.TricycleAchat.as_view(), name='payement'),
	path('reservation/', views.ReservationView.as_view(), name='reservation'),
	path('confirmation/', views.payement_view, name='confirmation'),
	path('contact/',views.contact,name='contact')
  
]