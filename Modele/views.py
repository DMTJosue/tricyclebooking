from django.shortcuts import render
from Tricycleapp.models import Modele, Tricycle
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from .forms import ModeleForm
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.



class ModeleDetail(DetailView):
    template_name = 'Modele/detail.html'
    model = Modele

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tricycles = Tricycle.objects.filter(modele=self.object)
        context['tricycles'] = tricycles
        return context

class ModeleListView(ListView):
	model = Modele
	template_name = 'Modele/list.html'
	context_object_name = 'modeles'


class ModeleCreateView(CreateView):
	model = Modele
	template_name = "Modele/create.html"
	form_class = ModeleForm
	success_url = reverse_lazy('modele:list')


class ModeleUpdateView(UpdateView):
	model = Modele
	template_name = "Modele/create.html"
	form_class = ModeleForm
	success_url = reverse_lazy('modele:list')


class ModeleDeleteView(DeleteView):
	model = Modele
	success_url = reverse_lazy('modele:list')