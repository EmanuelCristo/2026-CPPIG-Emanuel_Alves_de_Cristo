from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import SalaModelForm
from .models import Sala

class SalasView(ListView):
    model = Sala
    template_name = 'salas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(SalasView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)
        return qs

class SalaAddView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin,CreateView):
    model = Sala
    form_class = SalaModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala adicionada com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class SalaUpdateView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model = Sala
    form_class = SalaModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala atualizada com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()


class SalaDeleteView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin,DeleteView):
    model = Sala
    template_name = 'sala_apagar.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala apagada com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f"A sala {self.object} não pode ser excluida. "
                                    f"Essa sala está registrada em uma reserva.")

        return redirect(success_url)