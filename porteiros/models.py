from django.db import models
from stdimage import StdImageField


class Porteiro(models.Model):
    nome = models.CharField('Nome',max_length=50, help_text='Nome do porteiros')
    email = models.EmailField('Email',max_length=50, help_text='Email do porteiros')
    foto = StdImageField('Foto', upload_to='porteiros', help_text='Foto do porteiro')

    class Meta:
        verbose_name = 'porteiros'
        verbose_name_plural = 'Porteiros'

    def __str__(self):
       return self.nome