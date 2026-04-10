from django import forms

from .models import Chave

class ChaveModelForm(forms.ModelForm):
    class Meta:
        model = Chave
        fields = '__all__'