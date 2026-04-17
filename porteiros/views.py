from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from porteiros.models import Porteiro
from porteiros.forms import PorteiroModelForm

class PorteiroListView(ListView):
    model = Porteiro
    template_name = 'porteiros.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(PorteiroListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)
        return qs

class PorteiroAddView(SuccessMessageMixin, CreateView):
    model = Porteiro
    form_class = PorteiroModelForm
    template_name = 'porteiro_form.html'
    success_url = reverse_lazy('porteiros')
    success_message = 'Porteiro cadastrado com sucesso!'

class PorteiroUpdateView(SuccessMessageMixin, UpdateView):
    model = Porteiro
    form_class = PorteiroModelForm
    template_name = 'porteiro_form.html'
    success_url = reverse_lazy('porteiros')
    success_message = 'Porteiro atualizado com sucesso!'

class PorteiroDeleteView(SuccessMessageMixin, DeleteView):
    model = Porteiro
    template_name = 'porteiro_apagar.html'
    success_url = reverse_lazy('porteiros')
    success_message = 'Porteiro apagado com sucesso!'