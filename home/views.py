from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from reservas.models import Reserva


class IndexView(ListView):
    template_name = 'main.html'
    model = Reserva

    def get_queryset(self):
        hoje = timezone.localdate()
        buscar = self.request.GET.get('buscar')
        qs = super(IndexView, self).get_queryset().filter(status='A', inicioReserva__date=hoje)
        if buscar:
            qs = qs.filter(Q(chave__sala__nome__icontains=buscar) | Q(titular__nome__icontains=buscar))
        return qs

