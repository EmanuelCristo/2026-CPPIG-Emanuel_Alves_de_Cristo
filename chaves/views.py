from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ChaveModelForm
from .models import Chave

class ChavesView(ListView):
    model = Chave
    template_name = 'chaves.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ChavesView, self).get_queryset()
        if buscar:
            return qs.filter(nome__icontains=buscar)
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