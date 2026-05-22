from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from alunos.forms import AlunoModelForm
from alunos.models import Aluno


class AlunosView(ListView):
    model = Aluno
    template_name = 'alunos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(AlunosView, self).get_queryset()
        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar)|Q(matricula__icontains=buscar))
        return qs

class AlunoAddView(SuccessMessageMixin,CreateView):
    model = Aluno
    form_class = AlunoModelForm
    template_name = 'aluno_form.html'
    success_url = reverse_lazy('alunos')
    success_message = 'Aluno adicionado com sucesso!'

class AlunoUpdateView(SuccessMessageMixin,UpdateView):
    model = Aluno
    form_class = AlunoModelForm
    template_name = 'aluno_form.html'
    success_url = reverse_lazy('alunos')
    success_message = 'Aluno atualizado com sucesso!'

class AlunoDeleteView(SuccessMessageMixin,DeleteView):
    model = Aluno
    template_name = 'aluno_apagar.html'
    success_url = reverse_lazy('alunos')
    success_message = 'Aluno apagado com sucesso!'