from django.urls import path
from .views import RMAToJobCardView, RMACreateView, RMAListView, RMADetailView, RMAUpdateView, ConvertRMAToJobCardView, \
    RMAQueryView

urlpatterns = [
    path('<int:pk>/convert/<str:technician_name>/', RMAToJobCardView.as_view(), name='rma_to_jobcard'),
    path('create/', RMACreateView.as_view(), name='rma-create'),
    path('all/', RMAListView.as_view(), name='rma-list'),
    path('get/<int:pk>/', RMADetailView.as_view(), name='rma-detail'),
    path('update/<str:rmaNumber>/', RMAUpdateView.as_view(), name='rma-update'),
    path('convert/<str:rmaNumber>/<str:assignedTechnician>/', ConvertRMAToJobCardView.as_view(), name='rma-convert'),
    path('get/<str:rmaNumber>/', RMAQueryView.as_view(), name='rma-query'),

]
