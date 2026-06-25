from datetime import time
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet

from chaves.models import CopiaChave
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

    def clean_dataRetirada(self):
        data_retirada = self.cleaned_data.get('dataRetirada')
        agora = timezone.now()

        if data_retirada > agora:
            raise ValidationError("A data de retirada não pode ser no futuro.")
        return data_retirada

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

        chaves_reservadas = queryset_final.values_list('chave', flat=True)
        for form in self.forms:
            if 'reserva' in form.fields:
                if form.instance and form.instance.pk and getattr(form.instance, 'reserva', None):
                    form.fields['reserva'].queryset = Reserva.objects.filter(
                        pk=form.instance.reserva_id
                    )
                else:
                    form.fields['reserva'].queryset = queryset_final
            if 'copia' in form.fields:
                if form.instance and form.instance.pk and getattr(form.instance, 'copia', None):
                    form.fields['copia'].queryset = CopiaChave.objects.filter(
                        pk=form.instance.copia.id
                    )
                else:
                    form.fields['copia'].queryset = CopiaChave.objects.filter(
                        chave__in=chaves_reservadas,
                        status='D'
                    )

    def clean(self):
        super().clean()

        reservas_validas = 0
        data_retirada = self.instance.dataRetirada if self.instance and self.instance.pk else None
        titular_atual = None

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                reserva = form.cleaned_data.get('reserva')
                copia = form.cleaned_data.get('copia')

                if reserva:
                    reservas_validas += 1
                    titular_atual = reserva.titular

                    if data_retirada and data_retirada < reserva.inicioReserva:
                        form.add_error('reserva', "A data de retirada não pode ser antes do início da reserva")

                    if copia and reserva:
                        if copia.chave != reserva.chave:
                            form.add_error('copia', f"Essa cópia não pertence à {reserva.chave.sala}.")
                        if copia.status != 'D':
                            form.add_error('copia', "Esta cópia não está disponível.")
        if reservas_validas == 0:
            raise ValidationError(
                "Selecione pelo menos uma reserva para fazer o empréstimo"
            )

        if titular_atual:
            agora = timezone.now()

            possui_atrasos = Emprestimo.objects.filter(
                status='A',
                reservas__titular=titular_atual,
                reservas__fimReserva__lt=agora
            ).exists()

            if possui_atrasos:
                raise ValidationError(
                    f"Bloqueio: O usuário {titular_atual.nome} possui chaves com a devolução em atraso. "
                    f"É necessário realizar as devoluções pendentes para realizar novos emprestimos."
                )

class EmprestimoTerminadoForm(forms.ModelForm):
    ESTADO_CHAVE = (
        ('D', 'Disponíveis'),
        ('Q', 'Chave Quebrada'),
    )

    estado_chave = forms.ChoiceField(
        choices=ESTADO_CHAVE,
        label='Estado das Chaves',
        help_text='Verifique o estado das chaves',
    )

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

    def save(self, commit=True):
        emprestimo = super().save(commit=False)
        estado = self.cleaned_data.get('estado_chave')

        if commit:
            emprestimo.save()

            for vinculo in emprestimo.emprestimos_reserva_emprestimo.all():
                titular = vinculo.reserva.titular
                copia_fisica = vinculo.copia

                if estado == 'Q':
                    titular.quantidadeDanos += 1
                    if titular.quantidadeDanos >= 3:
                        titular.bloqueado = True
                    if copia_fisica:
                        copia_fisica.status = 'Q'
                        copia_fisica.save()
                else:
                    titular.quantidadeDanos = 0

                titular.save()

        return emprestimo

EmprestimoReservaInLine = inlineformset_factory(
    Emprestimo,
    EmprestimoReserva,
    formset=EmprestimoReservaFormSet,
    fields=('reserva', 'copia'),
    extra=1,
    can_delete=True,
)