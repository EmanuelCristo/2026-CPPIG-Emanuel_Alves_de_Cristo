from django import forms

from .models import Sala

class SalaModelForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O nome da sala é um campo obrigatorio', 'unique': 'nome já cadastrado'},
            'tipo': {'required': 'O tipo da sala é um campo obrigatorio'},
            'anexo': {'required': 'O anexo da sala é um campo obrigatorio'},
        }