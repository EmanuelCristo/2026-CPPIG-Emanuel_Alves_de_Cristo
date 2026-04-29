from django import forms
from django.forms import inlineformset_factory

from .models import Emprestimo, ReservaEmprestimo

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'

ReservaEmprestimoInline = inlineformset_factory(Emprestimo, ReservaEmprestimo, fields =('reserva',), extra=1, can_delete=True, )