from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'github_username', 'github_link', 'telegram_username']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'github_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Username'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/yourprofile'}),
            'telegram_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
