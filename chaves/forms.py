from django import forms

from .models import Chave, CopiaChave


class ChaveModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'

    def clean_quantidadeCopias(self):
        quantidade_nova = self.cleaned_data.get('quantidadeCopias')

        if self.instance and self.instance.pk:
            quantidade_atual = self.instance.quantidadeCopias

            if quantidade_nova < quantidade_atual:
                raise forms.ValidationError(
                    f"Não é permitido reduzir a quantidade de cópias. Esta chave possui {quantidade_atual} cópias."
                )
        return quantidade_nova

class CopiaChaveForm(forms.ModelForm):
    class Meta:
        model = CopiaChave
        fields = ('status', )
