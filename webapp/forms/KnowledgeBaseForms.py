from django import forms

from webapp.models import KnowledgeBase


class KnowledgeBaseForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ['title', 'content']
