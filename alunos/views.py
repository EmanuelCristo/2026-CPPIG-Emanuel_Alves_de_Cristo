from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from alunos.forms import AlunoModelForm
from alunos.models import Aluno

class AlunosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Aluno
    template_name = 'alunos.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(AlunosView, self).get_queryset()
        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar)|Q(matricula__icontains=buscar))
        return qs

class AlunoAddView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Aluno
    form_class = AlunoModelForm
    template_name = 'aluno_form.html'
    success_url = reverse_lazy('alunos')
    success_message = 'Aluno adicionado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class AlunoUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,UpdateView):
    model = Aluno
    form_class = AlunoModelForm
    template_name = 'aluno_form.html'
    success_url = reverse_lazy('alunos')
    success_message = 'Aluno atualizado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

class AlunoDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Aluno
    template_name = 'aluno_apagar.html'
    success_url = reverse_lazy('alunos')
    success_message = 'Aluno apagado com sucesso!'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name="Admins").exists()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f"O aluno {self.object} não pode ser excluido. "
                                    f"Esse aluno está registrado em uma reserva.")

        return redirect(success_url)