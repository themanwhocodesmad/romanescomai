
from django import forms

from authentication.models import CustomUser
from resources.models import Region, Products, ErrorCodes, Vendor
from system.models import JobCard, Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'contact_number', 'alt_contact_number', 'address']


class JobCardForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label='Region')
    vendor_name = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=False, label='Vendor')
    product_name = forms.ModelChoiceField(queryset=Products.objects.all(), required=False, label='Product')
    error_code = forms.ModelChoiceField(queryset=ErrorCodes.objects.all(), required=False, label='Error Code')
    assigned_technician = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role__in=[CustomUser.TECHNICAL_ADMIN, CustomUser.FIELD_TECHNICIAN]),
        required=True,
        label='Assigned Technician'
    )

    date_of_query = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_of_purchase = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = JobCard
        fields = ['complaint_or_query', 'error_code', 'date_of_query',
                  'date_of_purchase', 'region', 'vendor_name', 'product_name',
                  'serial_number', 'assigned_technician']
