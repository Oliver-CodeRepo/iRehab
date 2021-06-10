import doctor
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import datetime as dt

from doctor.models import Doctor


# Create your models here.


class Profile(models.Model):
    user_type = models.CharField(max_length=20, default='Patient')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    addiction = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    @classmethod
    def get_profile(cls, user_id):
        profile = cls.objects.get(id=user_id)
        return profile


class Record(models.Model):
    date_checked = models.DateTimeField(auto_now_add=True, null=True)
    problem = models.CharField(max_length=200)
    Recurrent = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_records(cls):
        records = cls.objects.all()
        return records


class Appointment(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    topic = models.CharField(max_length=200, blank=True, null=True)
    narrative = models.TextField()
    date_asked = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_questions(cls):
        questions = cls.objects.all()
        return questions

    @classmethod
    def get_specific_questions(cls, question_id):
        question = cls.objects.get(id=question_id)
        return question
        
    def get_absolute_url(self):
        return reverse('question', args=[str(self.pk)])


class Comment(models.Model):
    opinion = models.CharField(max_length=200, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name='quiz')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    

    @classmethod
    def get_comments(cls, question_id):
        comments = cls.objects.filter(question=question_id)
        return comments



class Session(models.Model):
    availability = models.BooleanField(default=True)
    sloted_date = models.DateTimeField(null=True, blank=True)
    duration = models.CharField(null=True, blank=True, max_length=50)
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sloted_date

    @classmethod
    def get_session(cls):
        sessions = cls.objects.filter(availability=True)
        return sessions

    @classmethod
    def get_booked_session(cls):
        sessions = cls.objects.filter(availability=False)
        return sessions


class Inpatient(models.Model):
    availability = models.BooleanField(default=True)
    starting_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True, max_length=50)
    problem = models.TextField(default='description...')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # status = models.BooleanField(default=False)

    @classmethod
    def get_vacancies(cls):
        vacancies = cls.objects.filter(availability=True)
        return vacancies

    @classmethod
    def get_booked_vacancies(cls):
        vacancies = cls.objects.filter(availability=False)
        return vacancies


class Reservation(models.Model):
    patient_type = models.CharField(null=True, blank=True, max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class UserAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    problem = models.TextField(max_length=255)
    scheduled = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

