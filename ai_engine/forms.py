from django import forms
from .models import SubjectNote, SharedResource, KcsePastPaper

class SubjectNoteForm(forms.ModelForm):
    class Meta:
        model = SubjectNote
        fields = ['subject', 'topic', 'file', 'description']

class SharedResourceForm(forms.ModelForm):
    class Meta:
        model = SharedResource
        fields = ['title', 'description', 'file']

class KcsePastPaperForm(forms.ModelForm):
    class Meta:
        model = KcsePastPaper
        fields = ['subject', 'year', 'paper_type', 'file', 'description']