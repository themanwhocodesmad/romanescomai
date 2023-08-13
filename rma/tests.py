from django.urls import path
from .views import RMACreateView

urlpatterns = [
    path('rma/', RMACreateView.as_view(), name='rma-create'),
]
