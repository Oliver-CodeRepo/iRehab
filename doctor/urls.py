from django.urls import path
from doctor.views import *

app_name = 'doctor'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('docApp/', docApp, name='docApp'),
    path('docApp/<int:app_id>', approveApp, name='approveApp'),

    path('docChat/', docChat, name='docChat'),

    path('auth/doctors-login', doctorloginPage, name='doctorLogin'),
    
    path('auth/doctors-register/', doctorRegPage, name='doctorRegister'),
    path('auth/doctors-logout/', doctorlogoutPage, name='doctorLogout'),
]