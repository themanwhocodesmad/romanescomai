# forms.py
from django import forms


class JobNumberForm(forms.Form):
    job_number = forms.CharField(label='Job Number')
