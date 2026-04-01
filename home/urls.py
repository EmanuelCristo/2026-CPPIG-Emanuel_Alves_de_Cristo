from django.urls import path

from salas.views import SalasView
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(),name='index'),
]