from django import forms

from .models import Servidor

class ServidorModelForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = "__all__"