from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer
from .models import Products, ErrorCodes
from .models import Region, Vendor
from .serializers import ProductsSerializer, ErrorCodesSerializer
from .serializers import RegionSerializer, VendorSerializer


# Django views.py


class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.filter(role=CustomUser.FIELD_TECHNICIAN)
    serializer_class = CustomUserSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('name')
    serializer_class = ProductsSerializer


class ErrorCodesViewSet(viewsets.ModelViewSet):
    queryset = ErrorCodes.objects.all().order_by('product__name', 'code')
    serializer_class = ErrorCodesSerializer


class RepairTypesView(APIView):

    def get(self, request, *args, **kwargs):
        REPAIR_CHOICES = {
            'Service Centre Repair': 'Service Centre Repair',
            'Field Repair': 'Field Repair'
        }
        return Response(REPAIR_CHOICES, status=status.HTTP_200_OK)

