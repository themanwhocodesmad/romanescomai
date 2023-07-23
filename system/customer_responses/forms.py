from django import forms


class CustomerSatisfactionForm(forms.Form):
    job_number = forms.CharField(widget=forms.HiddenInput(), required=True)  # This will hold the job number
    service_rating = forms.ChoiceField(choices=[("", "Choose...")] + [(str(i), str(i)) for i in range(1, 6)], required=True)  # 1-5 rating scale
    comments = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_rating'].initial = ""  # Sets the initial value to "Choose..."
