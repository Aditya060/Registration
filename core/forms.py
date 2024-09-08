from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'job', 'company', 'panel']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email Address', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Phone Number', 'required': True}),
            'job': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Job Title', 'required': True}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Company Name', 'required': False}),  # Make company optional
            'panel': forms.Select(attrs={'class': 'form-control'})
        }
