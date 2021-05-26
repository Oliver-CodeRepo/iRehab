from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from mainApp.models import UserAppointment
from doctor.models import Doctor


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


class RescheduleForm(forms.ModelForm):
    class Meta:
        model = UserAppointment
        fields = '__all__'

        widgets = {
            'user':forms.Select(attrs={'class':'form-control','readonly':'readonly'}),
            'doctor':forms.Select(attrs={'class':'form-control','readonly':'readonly'}),
            'problem':forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
            'scheduled':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime'}),
        }
        

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'