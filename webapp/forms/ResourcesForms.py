# forms.py
from django import forms
from resources.models import Products, ErrorCodes, Region, Vendor


# forms.py

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']


class VendorForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label='Region')

    class Meta:
        model = Vendor
        fields = ['name', 'region']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'stockcode']


class ErrorCodeForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all(), required=True, label='Product')

    class Meta:
        model = ErrorCodes
        fields = ['code', 'product']
