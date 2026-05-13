from django.db import models

import porteiros


class EmprestimoReserva(models.Model):
    emprestimo = models.ForeignKey(to='emprestimos.Emprestimo', verbose_name='Empréstimo', on_delete=models.CASCADE, related_name='emprestimos_reserva_emprestimo')
    reserva = models.ForeignKey(to='reservas.Reserva', verbose_name='Reserva', on_delete=models.PROTECT, related_name='emprestimos_reserva_reserva')

    class Meta:
        verbose_name = 'Reserva do Empréstimo'
        verbose_name_plural = 'Reservas do Empréstimo'

    def __str__(self):
        return f'{self.reserva}'

class Emprestimo(models.Model):
    dataRetirada = models.DateTimeField('Data de Retirada', help_text='Data da retirada')
    reservas = models.ManyToManyField(to='reservas.Reserva', through='emprestimos.EmprestimoReserva', related_name='emprestimo_reservas')
    porteiro = models.ForeignKey(porteiros.models.Porteiro, verbose_name='Porteiro', help_text='Porteiro que entregou a chave' ,on_delete=models.PROTECT, default=1)

    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'

    def __str__(self):
        return f'Empréstimo: {self.dataRetirada}'

class OrdemEmprestimo(models.Model):
    status = models.CharField('Status', help_text='Status da Devolução', default='D', null=True)
    dataDevolucao = models.DateTimeField('Data de Devolução', help_text='Data da devolução', null=True)
    emprestimo = models.ForeignKey('emprestimos.Emprestimo', verbose_name='Emprestimo', on_delete=models.CASCADE, related_name='ordem_emprestimos_emprestimo')