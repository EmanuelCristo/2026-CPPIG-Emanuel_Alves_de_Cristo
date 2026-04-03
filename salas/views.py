from django.contrib.messages.views import SuccessMessageMixin
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

class SalaAddView(SuccessMessageMixin,CreateView):
    model = Sala
    form_class = SalaModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala adicionada com sucesso!'

class SalaUpdateView(SuccessMessageMixin,UpdateView):
    model = Sala
    form_class = SalaModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala atualizada com sucesso!'

class SalaDeleteView(SuccessMessageMixin,DeleteView):
    model = Sala
    template_name = 'sala_apagar.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala apagada com sucesso!'