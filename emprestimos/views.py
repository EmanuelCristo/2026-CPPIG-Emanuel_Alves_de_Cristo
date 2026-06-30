from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .utils.scheduler import agendar_alerta

from emprestimos.forms import EmprestimoModelForm, EmprestimoReservaInLine, EmprestimoTerminadoForm
from emprestimos.models import Emprestimo

class EmprestimosListView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'

    def get_queryset(self):
        qs = super(EmprestimosListView, self).get_queryset().filter(status='A')
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(Q(reservas__titular__nome__icontains=buscar)|Q(reservas__chave__sala__nome=buscar))
        return qs

class EmprestimoAddView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Emprestimo criado com sucesso!'

    def test_func(self):
        usuario = self.request.user

        if usuario.is_superuser:
            return True

        grupos_permitidos = ['Admins', 'Porteiros']

        return usuario.groups.filter(name__in=grupos_permitidos).exists()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        buscar_pessoa = self.request.GET.get('buscar_pessoa', None)

        if self.request.POST:
            data['frm_inline'] = EmprestimoReservaInLine(
                self.request.POST,
                buscar_pessoa=buscar_pessoa
            )
        else:
            data['frm_inline'] = EmprestimoReservaInLine(
                buscar_pessoa=buscar_pessoa
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        frm_inline = context['frm_inline']

        with transaction.atomic():
            if frm_inline.is_valid():
                self.object = form.save()
                frm_inline.instance = self.object

                vinculos_salvos = frm_inline.save()

                for vinculo in vinculos_salvos:
                    if hasattr(vinculo, 'reserva'):
                        reserva = vinculo.reserva
                        reserva.status = 'R'
                        reserva.save()
                        agendar_alerta(reserva)

                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form, frm_inline=frm_inline))

class EmprestimoUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Emprestimo alterado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def get_queryset(self):
        return super().get_queryset().prefetch_related('emprestimos_reserva_emprestimo')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = EmprestimoReservaInLine(self.request.POST, instance=self.object)
        else:
            data['frm_inline'] = EmprestimoReservaInLine(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        frm_inline = context['frm_inline']
        with transaction.atomic():
            if frm_inline.is_valid():
                self.object = form.save()
                frm_inline.instance = self.object
                frm_inline.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

class EmprestimoFinalizarUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoTerminadoForm
    template_name = 'emprestimo_finalizar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Emprestimo concluido com sucesso!'

    def test_func(self):
        usuario = self.request.user

        if usuario.is_superuser:
            return True

        grupos_permitidos = ['Admins', 'Porteiros']

        return usuario.groups.filter(name__in=grupos_permitidos).exists()

class EmprestimosFinalizadosListView(ListView):
    model = Emprestimo
    template_name = 'emprestimos_finalizados.html'

    def get_queryset(self):
        qs = super(EmprestimosFinalizadosListView, self).get_queryset().exclude(status='A')
        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(Q(reservas__titular__nome__icontains=buscar)|Q(reservas__chave__sala__nome=buscar))
        return qs

class EmprestimoDeleteView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin, DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')
    success_message = 'Emprestimo excluído com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()
