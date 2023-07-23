from rest_framework import serializers
from .models import Products, ErrorCodes, Region, Vendor


class ErrorCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorCodes
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    error_codes = ErrorCodesSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ('name', 'stockcode', 'error_codes')


class VendorSerializer(serializers.ModelSerializer):
    regionName = serializers.ReadOnlyField(source='region.name')  # This gives you the region name
    regionId = serializers.ReadOnlyField(source='region.id')  # This gives you the region id

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'regionId', 'regionName']


class RegionSerializer(serializers.ModelSerializer):
    vendors = VendorSerializer(many=True, read_only=True)  # This gives you all vendors for a region

    class Meta:
        model = Region
        fields = ['id', 'name', 'vendors']


class RepairTypeSerializer(serializers.Serializer):
    repair_type = serializers.ChoiceField(choices=[
        ('Service Centre Repair'),
        ('Field Repair')
    ])
