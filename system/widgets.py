from django.forms.widgets import Textarea


class AppendableTextarea(Textarea):
    template_name = 'appendable_textarea.html'
