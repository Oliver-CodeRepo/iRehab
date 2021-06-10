from mainApp.forms import CommentForm, QuestionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.contrib import  messages
import africastalking
from django.views.generic import UpdateView

from doctor.forms import DoctorRegForm, ApproveForm, AvailabilityForm, RescheduleForm
from mainApp.models import *
from doctor.models import *

# Create your views here.

def doctorRegPage(request):
    if request.user.is_authenticated:
        return redirect('doctor:dashboard')
    else:
        form = DoctorRegForm()
        if request.method == 'POST':
            form = DoctorRegForm(request.POST)
            if form.is_valid():
                dform = form.save(commit=False)
                dform.is_staff = True
                dform.save()
                un = form.cleaned_data.get('username')
                messages.success(request, 'Account creation as doctor '+ un +' was successful.')
                return redirect('doctor:dashboard')
        else:
            form = DoctorRegForm()

        context = {'form': form}
        return render(request, 'authTemp/doctorRegister.html', context)


def doctorloginPage(request):
    if request.user.is_authenticated:
        return redirect('doctor:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff == True:
                print(user)
                login(request, user)
                return redirect('doctor:dashboard')
            else:
                messages.info(request, 'Wrong Username or Password')
                return redirect('doctor:doctorLogin')

        context = {}
        return render(request, 'authTemp/doctorLogin.html', context)


def doctorlogoutPage(request):
    logout(request)
    return redirect('doctor:doctorLogin')


@login_required(login_url='doctor:doctorLogin')
def dashboard(request):
    av_ap = Doctor.objects.filter(name=request.user.id).first()
    app = UserAppointment.objects.filter(doctor__id=av_ap.id, status=False).all().count()
    inapp = Inpatient.objects.filter(doctor__id=av_ap.id, availability=True).all().count()

    if 'action' in request.GET.keys():
        action = request.GET['action']
        if action == 'set_availability':
            av_ap = av_ap
            print(av_ap)
            if av_ap.availability == False:
                av_ap.availability = True
                av_ap.save()
                print('hhhh',av_ap)
                messages.info(request, 'Availability is set On')
                return redirect('doctor:dashboard')
            else:
                av_ap.availability = False
                av_ap.save()
                print('gggg',av_ap)
                messages.info(request, 'Availability is set Off')
                return redirect('doctor:dashboard')

    context = {'app':app, 'av_ap':av_ap, 'inapp':inapp}
    return render(request, 'doctor/dashboard.html', context)



@login_required(login_url='doctor:doctorLogin')
def docApp(request):
    user = Doctor.objects.filter(name=request.user.id).first()
    app = UserAppointment.objects.filter(doctor__id=user.id).order_by('-id')[:5]
    Inapp = Inpatient.objects.filter(doctor__id=user.id).order_by('-id')[:5]

    context = {'app':app, 'Inapp':Inapp}
    return render(request, 'doctor/docAppoint.html', context)


@login_required(login_url='doctor:doctorLogin')
def docChat(request):
    chats = Question.objects.all()
    

    context = {"chats":chats}
    return render(request, 'doctor/docChat.html', context)


@login_required(login_url='doctor:doctorLogin')
def addPost(request):
    
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor:docChat')
    else:
        form = QuestionForm()
    context = { 'form': form}
    return render(request, 'doctor/addDocPost.html', context)


@login_required(login_url='doctor:doctorLogin')
def qDetails(request, q_id):
    questions = Question.objects.filter(id=q_id)
    comments = Comment.objects.filter(question=q_id).order_by('-id')
    context = {'questions': questions, 'comments': comments}
    return render(request, 'doctor/postDetails.html', context)




@login_required(login_url='doctor:doctorLogin')
def comments(request, qd_id):
    current_question = Question.objects.get(id=qd_id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = current_question
            comment.save()
            return redirect('doctor:qDeatils', qd_id) 
    else:
        form = CommentForm()

    context = {'form': form, 'current_question': current_question}
    return render(request, 'doctor/comment.html', context)


@login_required(login_url='doctor:doctorLogin')
def approveApp(request, app_id):
    context = {}
    appToApprove = get_object_or_404(UserAppointment, id=app_id)
    approve = ApproveForm(request.POST or None, instance=appToApprove)
    

    if approve.is_valid():
        app = approve.save(commit=False)
        sc = appToApprove.scheduled
        u = appToApprove.user
        j = u.last_name
        problem = appToApprove.problem
        phone = [str(j)]
        

        username = 'rehab'
        apikey = 'b548d8868cd94d805e5d2437ce591bad511eb783cf8c3eb9e972449e5b14a52c'
        message = 'Hello ' + str(u)+ '\nYour Appointment on problem tagged "'+ str(problem) +'" was Approved for date '  + str(sc) +  ' by doctor ' + request.user.username + '.'
        # sender = '5196'

        africastalking.initialize(username, apikey)
        sms = africastalking.SMS
        response = sms.send(message, phone)
        print(response)

        app.save()
        messages.info(request, 'Appointment Approval was a success.')
        return redirect('doctor:docApp')

    context['approve'] = approve
    return render(request, 'doctor/approveApp.html', context)  


@login_required(login_url='doctor:doctorLogin')
def reschedule(request, rs_id):
    context = {}
    appToReschedule = get_object_or_404(UserAppointment, id=rs_id)
    rescheduleForm = RescheduleForm(request.POST or None, instance=appToReschedule)

    if rescheduleForm.is_valid():
        r = rescheduleForm.save(commit=False)
        sc = appToReschedule.scheduled
        u = appToReschedule.user
        j = u.last_name
        phone=[str(j)]

        username = 'rehab'
        apikey = 'b548d8868cd94d805e5d2437ce591bad511eb783cf8c3eb9e972449e5b14a52c'
        message = 'Hello ' + str(u) + '\nYour Appointment was Rescheduled to '  + str(sc) +  ' by doctor ' + request.user.username + '.'
        # sender = '5196'

        africastalking.initialize(username, apikey)
        sms = africastalking.SMS
        response = sms.send(message, phone)
        print(response)

        r.save()
        messages.info(request, 'Rescheduling was a success.')
        return redirect("doctor:docApp")

    context['rescheduleForm'] = rescheduleForm
    return render(request, 'doctor/reschedule.html', context)  



def aboutUsPage(request):
    context = {}
    return render(request, 'doctor/aboutUs.html', context)


def docProfile(request, user_id):
    context = {}
    userModel = get_object_or_404(User, id=user_id)
    form = DoctorRegForm(request.POST or None, instance=userModel)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile Updated was successfully.')
        return redirect('doctor:docProfile')

    context = {'form': form}
    return render(request, 'doctor/docProfile.html', context)
