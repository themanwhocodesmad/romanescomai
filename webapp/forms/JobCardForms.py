# forms.py
from django import forms
from django.forms import ModelForm, inlineformset_factory

from authentication.models import CustomUser
from resources.models import Region, Vendor, Products, ErrorCodes
from system.models import Customer
from system.models import Image, JobCard


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'contact_number', 'alt_contact_number', 'address']


class EditJobCardForm(forms.ModelForm):
    # region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label='Region')
    # vendor_name = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=False, label='Vendor')
    # product_name = forms.ModelChoiceField(queryset=Products.objects.all(), required=False, label='Product')
    # error_code = forms.ModelChoiceField(queryset=ErrorCodes.objects.all(), required=False, label='Error Code')

    # assigned_technician = forms.ModelChoiceField(
    #     queryset=CustomUser.objects.filter(role__in=[CustomUser.TECHNICAL_ADMIN, CustomUser.FIELD_TECHNICIAN]),
    #     required=True,
    #     label='Assigned Technician'
    # )

    date_of_technician_assessment = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
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
                  'date_of_purchase', 'date_of_technician_assessment' ,'region',
                  'serial_number', 'assigned_technician','technician_assessment',
                  'technician_notes',
                  'fault_code',
                  'job_type',
                  'follow_up_required']
        exclude = ['product_name', 'region', 'vendor_name', 'assigned_technician']


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description', 'sequence']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


# Create a formset for images linked to a JobCard
ImageFormSet = inlineformset_factory(JobCard, Image, form=ImageForm, extra=3, max_num=3, can_delete=False)
