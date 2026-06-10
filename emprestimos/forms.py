from datetime import time
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet

from reservas.models import Reserva
from .models import Emprestimo, EmprestimoReserva

class EmprestimoModelForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['dataRetirada', 'porteiroEntrega']
        widgets = {
            'dataRetirada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_inicioEmprestimo(self):
        data_retirada = self.cleaned_data.get('dataRetirada')
        agora = timezone.now()

        if data_retirada > agora:
            raise ValidationError("A data de retirada não pode ser no futuro.")
        return data_retirada

class EmprestimoReservaFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            if 'reserva' in form.fields:
                if form.instance and form.instance.pk and form.instance.reserva:
                    form.fields['reserva'].queryset = Reserva.objects.filter(
                        pk=form.instance.reserva_id
                    )
                else:
                    form.fields['reserva'].queryset = Reserva.objects.filter(status='A')

    def clean(self):
        cleaned_data = super().clean()

        reservas_validas = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('reserva'):
                    reservas_validas += 1

        if reservas_validas == 0:
            raise ValidationError(
                f"Selecione pelo menos uma reserva para fazer o empréstimo"
            )

class EmprestimoTerminadoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['dataDevolucao', 'porteiroDevolucao', 'status']
        widgets = {
            'dataDevolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            data_devolucao = cleaned_data.get('dataDevolucao')
            inicio_reserva = cleaned_data.get('inicioReserva')

            if data_devolucao and data_devolucao > timezone.now():
                raise ValidationError(
                    f"A data de devolução não pode ser feita no futuro."
                )

            if data_devolucao and data_devolucao < inicio_reserva:
                raise ValidationError(
                    "A devolução não pode ser feita antes do inicio da reserva"
                )


EmprestimoReservaInLine = inlineformset_factory(
    Emprestimo,
    EmprestimoReserva,
    formset=EmprestimoReservaFormSet,
    fields=('reserva', ),
    extra=1,
    can_delete=True,
)