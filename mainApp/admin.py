from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Record)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Inpatient)
admin.site.register(Reservation)
admin.site.register(UserAppointment)
