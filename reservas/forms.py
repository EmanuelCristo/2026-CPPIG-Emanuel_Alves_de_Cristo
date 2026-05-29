from datetime import time

from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError

from chaves.models import Chave
from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'inicioReserva': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
            'fimReserva': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     chaves = Chave.objects.filter(status='D').count()
    #     self.fields['chaves'].initial = chaves

    # def clean_inicioReserva(self):
    #     inicio = self.cleaned_data.get('inicioReserva')
    #     agora = timezone.now()
    #     horario_inicio = timezone.localtime(inicio).time()
    #
    #     if inicio < agora:
    #         raise ValidationError("O início da reserva não pode ser no passsado.")
    #
    #     if horario_inicio < time(8, 0) or horario_inicio > time(21, 30):
    #         raise ValidationError("As reservas só podem ser iniciadas entre as 8:00 e as 21:30")
    #
    #     return inicio
    #
    # def clean_fimReserva(self):
    #     fim = self.cleaned_data.get('fimReserva')
    #     horario_fim = timezone.localtime(fim).time()
    #
    #     if horario_fim < time(8, 0) or horario_fim > time(22, 00):
    #         raise ValidationError("A devolução só pode ser feita entre as 8:00 e as 22:00")
    #
    #     return fim
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     inicio = cleaned_data.get('inicioReserva')
    #     fim = cleaned_data.get('fimReserva')
    #
    #     if inicio and fim and fim <= inicio:
    #         raise ValidationError({
    #             'fimReserva': "A data/hora de fim deve ser posterior ao início da reserva.",
    #         })
    #     return cleaned_data