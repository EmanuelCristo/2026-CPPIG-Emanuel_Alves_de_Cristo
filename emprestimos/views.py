from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from emprestimos.forms import EmprestimoModelForm, ReservaEmprestimoInline
from emprestimos.models import Emprestimo

class EmprestimosListView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'

  #  def get_queryset(self):
   #     buscar = self.request.GET.get('buscar')
  #      qs = super(EmprestimosView, self).get_queryset()
   #
   #     if buscar:
    #        qs = qs.filter()

class EmprestimoAddView(SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    sucess_message = 'Emprestimo criado com sucesso!'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = ReservaEmprestimoInline(self.request.POST)
        else:
            data['frm_inline'] = ReservaEmprestimoInline()
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

class EmprestimoUpdateView(SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoModelForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')
    sucess_message = 'Emprestimo atualizado!'

    def get_queryset(self):
        return super().get_queryset().prefetche_related('reserva_emprestimo_emprestimo')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = ReservaEmprestimoInline(self.request.POST, instance=self.object)
        else:
            data['frm_inline'] = ReservaEmprestimoInline(instance=self.object)
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