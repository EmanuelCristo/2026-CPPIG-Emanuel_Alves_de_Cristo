from django.db.models import Q
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from reservas.forms import ReservaModelForm
from reservas.models import Reserva


class ReservasListView(ListView):
    model = Reserva
    template_name = 'reservas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservasListView, self).get_queryset().filter(status='A')
        if buscar:
            qs = qs.filter(Q(chave__sala__nome__icontains=buscar)|Q(titular__nome__icontains=buscar))
        return qs

class ReservaAddView(SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva criada com sucesso'

    def form_valid(self, form):
        response = super().form_valid(form)
        reserva = self.object

        dados = {
                'titular': reserva.titular.nome,
                'inicioReserva': reserva.inicioReserva.strftime('%d/%m/%Y'),
                'fimReserva': reserva.fimReserva.strftime('%d/%m/%Y'),
                'chave': reserva.chave,
                 }

        texto_email = render_to_string('emails/email_r_realizada.txt', dados)
        html_email = render_to_string('emails/email_r_realizada.html', dados)
        send_mail(subject='Reserva Realizada',
                  message=texto_email,
                  from_email='emanuelcristo7@gmail.com',
                  recipient_list=[reserva.titular.email],
                  html_message=html_email,
                  fail_silently=False,
                  )
        return response

class ReservaUpdateView(SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva atualizada com sucesso'

class ReservaDeleteView(SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva apagada com sucesso'

class ReservasFinalizadasListView(ListView):
    model = Reserva
    template_name = 'reservas_finalizadas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservasFinalizadasListView, self).get_queryset()
        if buscar:
            qs = qs.filter(Q(chave__sala__nome__icontains=buscar)|Q(titular__nome__icontains=buscar))
        return qs

