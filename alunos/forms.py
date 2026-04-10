from django import forms

from .models import Aluno

class AlunoModelForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = "__all__"