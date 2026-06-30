from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from servidores.models import Servidor
from servidores.forms import ServidorModelForm


class ServidoresView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Servidor
    template_name = 'servidores.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ServidoresView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)
        return qs

class ServidorAddView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,CreateView):
    model = Servidor
    form_class = ServidorModelForm
    template_name = 'servidor_form.html'
    success_url = reverse_lazy('servidores')
    success_message = 'Servidor adicionado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class ServidorUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model = Servidor
    form_class = ServidorModelForm
    template_name = 'servidor_form.html'
    success_url = reverse_lazy('servidores')
    success_message = 'Servidor atualizado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class ServidorDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    model = Servidor
    template_name = 'servidor_apagar.html'
    success_url = reverse_lazy('servidores')
    success_message = 'Servidor apagado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f"O servidor {self.object} não pode ser excluido. "
                                    f"Esse servidor está registrado em uma reserva.")

        return redirect(success_url)