from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

scheduler = BackgroundScheduler()


def dispara_alerta(reserva):
    from emprestimos.models import Emprestimo

    emprestimo_ativo = Emprestimo.objects.filter(reservas=reserva, status='A').exists()

    if emprestimo_ativo:
        assunto = f'ALERTA: Atraso Grave de 24 horas - Sala {reserva.chave.sala.nome}'

        prazo_original = timezone.localtime(reserva.fimReserva).strftime('%d/%m/%Y às %H:%M')

        mensagem = (
            f"Atenção\n\n"
            f"O usuário {reserva.titular.nome} ({reserva.titular.email}) está com a devolução da chave "
            f"da sala {reserva.chave.sala.nome} atrasada em mais de 24 horas.\n\n"
            f"Prazo original estipulado: {prazo_original}.\n\n"
            f"Por favor, entre em contato com o usuário ou tome as providências de bloqueio manual, se necessário.\n"
        )
        send_mail(
            assunto,
            mensagem,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )


def agendar_alerta(reserva):
    run_date = reserva.fimReserva + timedelta(minutes=1)

    if run_date > timezone.now():
        scheduler.add_job(
            dispara_alerta,
            'date',
            run_date=run_date,
            args=[reserva],
            id=f'alerta_atraso_{reserva.id}',
            replace_existing=True
        )
        print(f"Reserva {reserva.id} atrasada.")

def start():
    if not scheduler.running:
        scheduler.start()

def cancelar_reserva_atrasada(reserva_id):
    from reservas.models import Reserva

    try:
        reserva = Reserva.objects.get(id=reserva_id)
        if reserva.status == 'A':
            reserva.status = 'C'
            reserva.save()
            print(f"Reserva {reserva.id} cancelada por atraso de 15 minutos.")

    except Reserva.DoesNotExist:
        pass

def agendar_cancelamento(reserva):
    run_date = reserva.inicioReserva + timedelta(minutes=15)

    if run_date > timezone.now():
        scheduler.add_job(
            cancelar_reserva_atrasada,
            'date',
            run_date=run_date,
            args=[reserva.id],
            id=f'cancela_reserva_{reserva.id}',
            replace_existing=True
        )