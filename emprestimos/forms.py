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
        input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'],
        widgets = {
            'dataRetirada': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        }

    def clean_inicioEmprestimo(self):
        data_retirada = self.cleaned_data.get('dataRetirada')
        agora = timezone.now()

        if data_retirada > agora:
            raise ValidationError("A data de retirada não pode ser no futuro.")
        return data_retirada

    def clean(self):
        cleaned_data = super().clean()
        data_retirada = cleaned_data.get('dataRetirada')

        if self.instance.pk and data_retirada:
            lista_reservas = Reserva.objects.filter(
                emprestimo_reservas=self.instance
            )
            for reserva_obj in lista_reservas:
                if data_retirada < reserva_obj.inicioReserva:
                    raise ValidationError(
                        f"A data de retirada não pode ser antes do início da reserva"
                    )

        return cleaned_data

class EmprestimoReservaFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        buscar_pessoa = kwargs.pop('buscar_pessoa', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            primeira_reserva = self.instance.reservas.first()

            if primeira_reserva and primeira_reserva.titular:
                queryset_final = Reserva.objects.filter(
                    status='A',
                    titular=primeira_reserva.titular,
                )
            else:
                queryset_final = Reserva.objects.none()

        else:
            if buscar_pessoa:
                queryset_final = Reserva.objects.filter(
                    status='A',
                    titular__nome__icontains=buscar_pessoa
                )
            else:
                queryset_final = Reserva.objects.none()

        for form in self.forms:
            if 'reserva' in form.fields:
                if form.instance and form.instance.pk and getattr(form.instance, 'reserva', None):
                    form.fields['reserva'].queryset = Reserva.objects.filter(
                        pk=form.instance.reserva_id
                    )
                else:
                    form.fields['reserva'].queryset = queryset_final

    # def clean(self):
    #     super().clean()
    #
    #     reservas_validas = 0
    #     data_retirada = self.instance.dataRetirada if self.instance and self.instance.pk else None
    #
    #     for form in self.forms:
    #         if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
    #             reserva = form.cleaned_data.get('reserva')
    #             # titular_emprestimo = form.cleaned_data.get('reserva__titular')
    #             if reserva:
    #                 reservas_validas += 1
    #
    #                 if data_retirada and data_retirada < reserva.inicioReserva:
    #                     raise ValidationError(
    #                         f"A data de retirada não pode ser antes do início da reserva"
    #                     )
    #
    #                 # form.fields['reserva'].queryset = Reserva.objects.filter(titular=titular_emprestimo)
    #
    #
    #     if reservas_validas == 0:
    #         raise ValidationError(
    #             "Selecione pelo menos uma reserva para fazer o empréstimo"
    #         )

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
        data_retirada = self.instance.dataRetirada if self.instance else None

        if data_devolucao and data_devolucao > timezone.now():
            raise ValidationError(
                f"A data de devolução não pode ser feita no futuro."
            )

        if data_devolucao and data_retirada and data_devolucao < data_retirada:
            raise ValidationError(
                "A devolução não pode ser feita antes da retirada da chave."
            )

        return cleaned_data


EmprestimoReservaInLine = inlineformset_factory(
    Emprestimo,
    EmprestimoReserva,
    formset=EmprestimoReservaFormSet,
    fields=('reserva', ),
    extra=1,
    can_delete=True,
)