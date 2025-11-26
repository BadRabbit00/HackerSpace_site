from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Short description for the card...',
            'rows': 3,
            'style': 'background: #111; color: #fff; border: 1px solid #333;'
        }),
        label="Card Description"
    )

    class Meta:
        model = News
        fields = ['title', 'description', 'photo', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter news title',
                'style': 'background: #111; color: #fff; border: 1px solid #333;'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your content here...',
                'rows': 10,
                'style': 'background: #111; color: #fff; border: 1px solid #333;'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'style': 'background: #111; color: #fff; border: 1px solid #333;'
            }),
        }
