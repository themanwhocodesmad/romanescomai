from django import forms
from system.models import JobCard


class CloseJobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ['resolution', 'additional_notes']

