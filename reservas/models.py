from datetime import timedelta

from django.db import models
from django.db.models import Choices
from django.utils import timezone

from alunos.models import Aluno
from chaves.models import Chave
from servidores.models import Pessoa, Servidor

SITUACAO_OPCOES = (
        ('A', 'Agendado'),
        ('R', 'Realizado'),
        ('C', 'Cancelado'),
    )

class Reserva(models.Model):
    chave = models.ForeignKey(Chave, verbose_name='Chave', on_delete=models.PROTECT, help_text='Chave que deseja reservar')
    inicioReserva = models.DateTimeField(verbose_name='Inicio da Reserva', help_text='Data de inicio da reserva')
    fimReserva = models.DateTimeField(verbose_name='Fim da Reserva', help_text='Data de fim da reserva')
    titular = models.ForeignKey(Servidor, verbose_name='Titular' ,on_delete=models.PROTECT, help_text='Titular da reserva')
    status = models.CharField('Status', max_length=1, help_text='Status da reserva', choices=SITUACAO_OPCOES ,default='A')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.titular} - {self.chave} ( {timezone.localtime(self.inicioReserva).strftime('%d/%m/%Y %H:%M')} a {timezone.localtime(self.fimReserva).strftime('%d/%m/%Y %H:%M')} )"

