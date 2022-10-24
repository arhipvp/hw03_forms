from django import forms
from django.contrib.auth import get_user_model

from .models import Post

User = get_user_model()


class CreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['text', 'group', ]
        Widget = {
            'text': forms.Textarea(attrs={'class': 'form-input', }),
            'group': forms.ChoiceField(required=False, )
        }
