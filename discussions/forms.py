from django import forms
from .models import ThreadMessage, PrivateMessage

class ThreadMessageForm(forms.ModelForm):
    class Meta:
        model = ThreadMessage
        fields = ['content', 'media']


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['recipient', 'content', 'media']



class ReplyMessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Reply Content')