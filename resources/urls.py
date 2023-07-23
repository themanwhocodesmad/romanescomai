from django.urls import path

from .views import RegionViewSet, VendorViewSet, TechnicianViewSet, ProductsViewSet, ErrorCodesViewSet, RepairTypesView

urlpatterns = [
    path('products/', ProductsViewSet.as_view({'get': 'list'})),
    path('errorcodes/', ErrorCodesViewSet.as_view({'get': 'list'})),
    path('regions/', RegionViewSet.as_view({'get': 'list'})),
    path('vendors/', VendorViewSet.as_view({'get': 'list'})),
    path('technicians/', TechnicianViewSet.as_view({'get': 'list'})),
    path('repairtypes/', RepairTypesView.as_view(), name='repair-types'),
]