from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, widgets
from .models import Comment, Inpatient, Profile, Question, Record, UserAppointment


class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name','last_name']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class':'form-control', 'autofocus':'false'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Names', 'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'placeholder':'+2547.....', 'class':'form-control','type':'tel'}),
            'email': forms.TextInput(attrs={'placeholder': 'E-mail', 'class':'form-control'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Password', 'class':'form-control', 'type':'password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirm Password', 'class':'form-control', 'type':'password'}),
        }


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'

#         widgets = {
#             'user_type': forms.TextInput(attrs={'class':'form-control mb-2'}),
#             'first_name': forms.TextInput(attrs={'class':'form-control mb-2','placeholder': 'First Name','class':'form-control'}),
#             'last_name': forms.TextInput(attrs={'class':'form-control mb-2','placeholder': 'Last Name'}),
#             'phone': forms.TextInput(attrs={'class':'form-control mb-2','placeholder': 'Phone Number'}),
#             'addiction': forms.TextInput(attrs={'class':'form-control mb-2','placeholder': 'Addiction'}),
#             'user': forms.TextInput(attrs={'class':'form-control mb-2',}),
#         }


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

        widgets = {
            'topic': forms.TextInput(attrs={'placeholder': 'Add your opinion', 'class':'form-control'}),
            'narrative': forms.Textarea(attrs={'placeholder': 'Description', 'type':'hidden', 'class':'form-control'}),
            'date_asked': forms.TextInput(attrs={'type':'hidden'}),
            'user': forms.TextInput(attrs={'type':'hidden'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

        widgets = {
            'opinion': forms.TextInput(attrs={'placeholder': 'Add your opinion', 'class':'form-control'}),
            'date_posted': forms.TextInput(attrs={'placeholder': 'E-mail', 'type':'hidden'}),
            'question': forms.TextInput(attrs={'placeholder': 'Password', 'type':'hidden'}),
            'user': forms.TextInput(attrs={'placeholder': 'Confirm Password', 'type':'hidden'}),
        }


class UserAppointmentForm(forms.ModelForm):
    class Meta:
        model = UserAppointment
        fields = ['user','doctor','problem', 'scheduled']

        widgets = {
            'user': forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}),
            'doctor': forms.Select(attrs={'class':'form-control'}),
            'problem': forms.Textarea(attrs={'class':'form-control'}),
        }


class InpatientForm(forms.ModelForm):
    class Meta:
        model = Inpatient
        fields = ['doctor','problem','user','starting_date','finish_date']