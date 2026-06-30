from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from porteiros.models import Porteiro
from porteiros.forms import PorteiroModelForm

class PorteiroListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Porteiro
    template_name = 'porteiros.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(PorteiroListView, self).get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs

class PorteiroAddView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = Porteiro
    form_class = PorteiroModelForm
    template_name = 'porteiro_form.html'
    success_url = reverse_lazy('porteiros')
    success_message = 'Porteiro cadastrado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class PorteiroUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Porteiro
    form_class = PorteiroModelForm
    template_name = 'porteiro_form.html'
    success_url = reverse_lazy('porteiros')
    success_message = 'Porteiro atualizado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class PorteiroDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, DeleteView):
    model = Porteiro
    template_name = 'porteiro_apagar.html'
    success_url = reverse_lazy('porteiros')
    success_message = 'Porteiro apagado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()