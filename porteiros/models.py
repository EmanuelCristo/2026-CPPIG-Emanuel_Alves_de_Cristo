from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField


class Porteiro(models.Model):
    nome = models.CharField('Nome',max_length=50, help_text='Nome do porteiros')
    email = models.EmailField('Email',max_length=50, help_text='Email do porteiros', unique=True)
    cpf = models.CharField('CPF', max_length=14, help_text='CPF do porteiro', unique=True, null=True, blank=False)
    foto = StdImageField('Foto', upload_to='porteiros', help_text='Foto do porteiro')

    class Meta:
        verbose_name = 'porteiros'
        verbose_name_plural = 'Porteiros'
        ordering = [Upper('nome')]

    def __str__(self):
       return self.nome