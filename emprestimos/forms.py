from django import forms
from django.forms import inlineformset_factory
from .models import Emprestimo, EmprestimoReserva

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['dataRetirada', 'dataDevolucao']

EmprestimoReservaInLine = inlineformset_factory(
    Emprestimo,
    EmprestimoReserva,
    fields=('reserva',),
    extra=1,
    can_delete=True
)