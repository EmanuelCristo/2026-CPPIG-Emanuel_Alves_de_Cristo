from django.views.generic import TemplateView, ListView

import reservas


class IndexView(TemplateView):
    template_name = 'main.html'

class IndexListView(ListView):
    model = reservas
    template_name = 'main.html'
