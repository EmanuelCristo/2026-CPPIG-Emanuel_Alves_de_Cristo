from datetime import time

from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError

from chaves.models import Chave, CopiaChave
from .models import Reserva

class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'inicioReserva': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
            'fimReserva': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
        }

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['chave'].queryset = Chave.objects.filter(
             copiachave__status='D'
         ).distinct()


    def clean_inicioReserva(self):
         inicio = self.cleaned_data.get('inicioReserva')
         agora = timezone.now()
         horario_inicio = timezone.localtime(inicio).time()

         if inicio < agora:
             raise ValidationError("O início da reserva não pode ser no passsado.")

    #  if horario_inicio < time(8, 0) or horario_inicio > time(21, 30):
             raise ValidationError("As reservas só podem ser iniciadas entre as 8:00 e as 21:30")

         return inicio

    def clean_fimReserva(self):
         fim = self.cleaned_data.get('fimReserva')
         horario_fim = timezone.localtime(fim).time()

         if horario_fim < time(8, 0) or horario_fim > time(22, 00):
             raise ValidationError("A devolução só pode ser feita entre as 8:00 e as 22:00")

         return fim

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicioReserva')
        fim = cleaned_data.get('fimReserva')
        chave_selecionada = cleaned_data.get('chave')

        if inicio and fim and fim <= inicio:
            raise ValidationError({
                'fimReserva': "A data/hora de fim deve ser posterior ao início da reserva.",
            })

        if inicio and fim and chave_selecionada:
            total_copias_existentes = chave_selecionada.copiachave_set.filter(status='D').count()

            reservas_concorrentes = Reserva.objects.filter(
                chave=chave_selecionada,
                inicioReserva__lt=fim,
                fimReserva__gt=inicio
            )

            if self.instance.pk:
                reservas_concorrentes = reservas_concorrentes.exclude(pk=self.instance.pk)

            quantidade_reservas_ativas = reservas_concorrentes.count()

            if quantidade_reservas_ativas >= total_copias_existentes:
                raise ValidationError(
                    f"Não há mais cópias disponíveis para este horário. "
                    f"Todas as {total_copias_existentes} cópias já foram reservadas por outras pessoas."
                )

        return cleaned_data