from django import forms

from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'inicioReserva': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
            'fimReserva': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
        }