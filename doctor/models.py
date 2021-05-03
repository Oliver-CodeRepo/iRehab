from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Doctor(models.Model):
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor')
    availability = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)



