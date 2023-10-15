# forms.py
from django import forms

from system.models import JobCard


class JobCardQueryForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ['job_number']  # assuming job_number is a field in your JobCard model


class JobHistoryForm(forms.Form):
    job_number = forms.CharField(label='Job Number', max_length=20)
