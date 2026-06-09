from django.contrib import admin
from django.utils.html import format_html

from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'matricula')
    search_fields = ('nome', 'matricula')

    readonly_fields = ['foto']

    def foto(self, obj):
        if obj.foto:
            return format_html('<img width="75px" src="{}" />'.obj.foto.url)
        pass