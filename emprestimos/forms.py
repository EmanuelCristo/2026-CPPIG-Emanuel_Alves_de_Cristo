from datetime import timezone

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Emprestimo, EmprestimoReserva

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['dataRetirada', 'porteiroEntrega']
        widgets = {
            'dataRetirada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()


class EmprestimoTerminadoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['dataDevolucao', 'porteiroDevolucao', 'status']
        widgets = {
            'dataDevolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

EmprestimoReservaInLine = inlineformset_factory(
    Emprestimo,
    EmprestimoReserva,
    fields=('reserva',),
    extra=1,
    can_delete=True,
)