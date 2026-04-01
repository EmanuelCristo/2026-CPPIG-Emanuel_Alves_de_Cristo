from django.db import models

class Sala(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Nome da sala', unique=True)
    tipo = models.CharField('Tipo', max_length=100, help_text='Tipo da sala')
    anexo = models.CharField('Anexo', max_length=100, help_text='Anexo da sala')

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return self.nome