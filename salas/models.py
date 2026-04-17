from django.core.validators import RegexValidator
from django.db import models


ESCOLHER_ANEXO = (
    ('CT', 'Prédio Principal - Centro de Tecnologia'),
    ('A', 'Anexo A - CT'),
    ('B', 'Anexo B - CT'),
    ('C', 'Anexo C - CT'),
)

TIPO_SALA = (
    ('Sala de aula','Sala de aula'),
    ('Sala comunitária', 'Sala comunitária')
)

class Sala(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Nome da sala', unique=True, validators=[RegexValidator(regex=r'^\d{3,3}$',)])
    tipo = models.CharField('Tipo', max_length=100, choices=TIPO_SALA ,help_text='Tipo da sala')
    anexo = models.CharField('Anexo', max_length=30, choices=ESCOLHER_ANEXO, help_text='Anexo da sala')

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return self.nome