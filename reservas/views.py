from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, ProtectedError
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from reservas.forms import ReservaModelForm
from reservas.models import Reserva
from emprestimos.utils.scheduler import agendar_cancelamento


class ReservasListView(ListView):
    model = Reserva
    template_name = 'reservas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservasListView, self).get_queryset().filter(status='A')
        if buscar:
            qs = qs.filter(Q(chave__sala__nome__icontains=buscar)|Q(titular__nome__icontains=buscar))
        return qs

class ReservaAddView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva criada com sucesso'

    def test_func(self):
        usuario = self.request.user

        if usuario.is_superuser:
            return True

        grupos_permitidos = ['Admins', 'Servidores', 'Alunos']

        return usuario.groups.filter(name__in=grupos_permitidos).exists()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        agendar_cancelamento(self.object)
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
                  from_email='projetochaves7@gmail.com',
                  recipient_list=[reserva.titular.email],
                  html_message=html_email,
                  fail_silently=False,
                  )
        return response

class ReservaUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaModelForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva atualizada com sucesso'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class ReservaDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    sucess_message = 'Reserva apagada com sucesso'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f"A reserva {self.object} não pode ser excluida. "
                                    f"Essa reserva está registrada em um empréstimo.")

        return redirect(success_url)

class ReservasFinalizadasListView(ListView):
    model = Reserva
    template_name = 'reservas_finalizadas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservasFinalizadasListView, self).get_queryset().exclude(status='A')
        if buscar:
            qs = qs.filter(Q(chave__sala__nome__icontains=buscar)|Q(titular__nome__icontains=buscar))
        return qs

