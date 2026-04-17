from django import forms

from .models import Porteiro

class PorteiroModelForm(forms.ModelForm):
    class Meta:
        model = Porteiro
        fields = "__all__"