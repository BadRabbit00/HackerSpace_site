from django import forms
from .models import PersonalData

class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = ['full_name', 'iin', 'address', 'document_scan_front', 'document_scan_back', 'student_document']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'iin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IIN'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'document_scan_front': forms.FileInput(attrs={'class': 'form-control-file'}),
            'document_scan_back': forms.FileInput(attrs={'class': 'form-control-file'}),
            'student_document': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
