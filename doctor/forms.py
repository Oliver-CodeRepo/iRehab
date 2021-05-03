from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from mainApp.models import UserAppointment


class DoctorRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'doctor Ref Number'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Names'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'speciality'}),
            'email': forms.TextInput(attrs={'placeholder': 'E-mail'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirm Password'}),
        }


class ApproveForm(forms.ModelForm):
    class Meta:
        model = UserAppointment
        fields = ['status']

        