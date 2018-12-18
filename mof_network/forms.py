from django import forms
from django.contrib.auth.models import User
from .models import *


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textInput'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postContent'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textInput'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }


class MofForm(forms.ModelForm):

    class Meta:
        model = Mof
        fields = ('name', 'lcd', 'pld', 'area', 'density', 'formula', 'space_group', 'vol_frac', 'fingerprint')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textInput'}),
            'lcd': forms.NumberInput(attrs={'class': 'NumberInput'}),
            'pld': forms.NumberInput(attrs={'class': 'NumberInput'}),
            'area': forms.NumberInput(attrs={'class': 'NumberInput'}),
            'density': forms.NumberInput(attrs={'class': 'NumberInput'}),
            'formula': forms.TextInput(attrs={'class': 'textInput'}),
            'space_group': forms.TextInput(attrs={'class': 'textInput'}),
            'vol_frac': forms.NumberInput(attrs={'class': 'textInput'})
        }
