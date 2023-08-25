from django import forms
from .models import Board, Sticky

class BoardForm(forms.ModelForm):
    body = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                "placeholder": "Your board description",
                "class": "form-control",
                "rows": "3",
            }
            ),
            label="",
        )
    class Meta:
        model = Board
        fields = ['title', 'body']

class StickyForm(forms.ModelForm):
    body = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                "placeholder": "Your sticky description",
                "class": "form-control",
            }
            ),
            label="",
        )
    class Meta:
        model = Sticky
        fields = ['title', 'body']