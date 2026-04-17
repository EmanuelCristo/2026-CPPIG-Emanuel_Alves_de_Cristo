from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from reservas.forms import ReservaModelForm
from reservas.models import Reserva


class ReservasListView(ListView):
    model = Reserva
    template_name = 'reservas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservasListView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)
        return qs

class ReservaAddView(SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva criada com sucesso'

class ReservaUpdateView(SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva atualizada com sucesso'

class ReservaDeleteView(SuccessMessageMixin, DeleteView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva apagada com sucesso'
