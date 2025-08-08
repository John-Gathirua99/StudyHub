from django import forms
from .models import StudentAnswer

class StudentAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = ['answer_text']
        widgets = {
            'answer_text': forms.Textarea(attrs={'rows': 3})
        }

from django import forms
from .models import ExamFileMessage

class ExamFileMessageForm(forms.ModelForm):
    class Meta:
        model = ExamFileMessage
        fields = ['file', 'message']