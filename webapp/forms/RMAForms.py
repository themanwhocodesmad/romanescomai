# forms.py
from django import forms

from authentication import models
from authentication.models import CustomUser
from resources.models import Products
from rma.models import RMA


# forms.py
# forms.py

class EditRMAForm(forms.ModelForm):
    class Meta:
        model = RMA
        fields = '__all__'

class ConvertRMAForm(forms.ModelForm):
    technician = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role__in=[CustomUser.TECHNICAL_ADMIN, CustomUser.FIELD_TECHNICIAN]),
        required=True, label='Technician')
    received_at_warehouse = forms.BooleanField(required=False)
    convert_to_jobcard = forms.BooleanField(required=False)

    class Meta:
        model = RMA
        fields = ['received_at_warehouse', 'convert_to_jobcard', 'technician']


class RMAForm(forms.ModelForm):
    item_code = forms.ModelChoiceField(queryset=Products.objects.all(), label='Product Name')
    class Meta:
        model = RMA
        fields = ['item_code','date_returned', 'company_name', 'contact_person','reason', 'customer_name',
                  'contact_number', 'email_address', 'inv_no', 'inv_date',
                  'serial_no','package_condition', 'goods_condition', 'action','service_centre',
                   'customer_signature', 'received_at_warehouse',
                  'converted_or_closed']
