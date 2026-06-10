from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ChaveModelForm, CopiaChaveForm
from .models import Chave, CopiaChave


class ChavesListView(ListView):
    model = Chave
    template_name = 'chaves.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ChavesListView, self).get_queryset()
        if buscar:
            qs = qs.filter(Q(sala__nome__icontains=buscar)|Q(sala__anexo__icontains=buscar))
        return qs

class ChaveAddView(SuccessMessageMixin,CreateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave adicionada com sucesso!'

class ChaveUpdateView(SuccessMessageMixin,UpdateView):
    model = Chave
    form_class = ChaveModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave atualizada com sucesso!'

class ChaveDeleteView(SuccessMessageMixin,DeleteView):
    model = Chave
    template_name = 'chave_apagar.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave apagada com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f"A chave {self.object} não pode ser excluida. "
                                    f"Essa chave está registrada em uma reserva.")

        return redirect(success_url)

class CopiasChaveListView(SuccessMessageMixin,ListView):
    model = CopiaChave
    template_name = 'chave_copias.html'

    def get_queryset(self):
        chave_id = self.kwargs.get('pk')
        return CopiaChave.objects.filter(chave_id=chave_id)

class CopiasChaveUpdateView(SuccessMessageMixin,UpdateView):
    model = CopiaChave
    form_class = CopiaChaveForm
    template_name = 'copia_form.html'
    success_message = 'Copia atualizada com sucesso!'

    def get_success_url(self):
        return reverse_lazy('chave_copias', kwargs={'pk': self.object.chave.pk})

class CopiasChaveDeleteView(SuccessMessageMixin,DeleteView):
    model = CopiaChave
    template_name = 'copia_apagar.html'
    success_message = 'Copia apagada com sucesso!'

    def get_success_url(self):
        chave_pai_id = self.object.chave.pk
        return reverse_lazy('chave_copias', kwargs={'pk': chave_pai_id})