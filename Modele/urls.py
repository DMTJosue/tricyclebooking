from django.urls import path
from . import views


app_name = 'Modele'


urlpatterns = [
	# post views
	path('<int:pk>/', views.ModeleDetail.as_view(), name='detail'),
	path('', views.ModeleListView.as_view(), name='list'),
	path('add/', views.ModeleCreateView.as_view(), name='add'),
	path('update/<int:pk>/', views.ModeleUpdateView.as_view(), name='update'),
	path('delete/<int:pk>/', views.ModeleDeleteView.as_view(), name="delete")
]