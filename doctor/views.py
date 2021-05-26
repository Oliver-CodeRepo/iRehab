from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.contrib import  messages

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

            if user is not None:
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
    app = UserAppointment.objects.filter(doctor__id=request.user.id, status=True).all().count()

    if 'action' in request.GET.keys():
        action = request.GET['action']
        if action == 'set_availability':
            av_ap = Doctor.objects.filter(name=request.user.id).all()
            print(av_ap)
            if av_ap.availability is False:
                for a in av_ap:
                    a.availability = True
                    a.save()
                    print('hhhh',a)
                    messages.info(request, 'Availability is set On')
                return redirect('doctor:dashboard')
            else:
                for a in av_ap:
                    a.availability = False
                    a.save()
                    print('gggg',a)
                    messages.info(request, 'Availability is set Off')
                return redirect('doctor:dashboard')

    context = {'app':app}
    return render(request, 'doctor/dashboard.html', context)


@login_required(login_url='doctor:doctorLogin')
def docApp(request):
    app = UserAppointment.objects.filter(doctor__id=request.user.id)
    print(app)

    context = {'app':app}
    return render(request, 'doctor/docAppoint.html', context)


@login_required(login_url='doctor:doctorLogin')
def docChat(request):
    chats = Question.objects.all()
    context = {"chats":chats}
    return render(request, 'doctor/docChat.html', context)


@login_required(login_url='doctor:doctorLogin')
def approveApp(request, app_id):
    context = {}
    appToApprove = get_object_or_404(UserAppointment, id=app_id)
    approve = ApproveForm(request.POST or None, instance=appToApprove)

    if approve.is_valid():
        approve.save()
        messages.info(request, 'Approval was a success.')
        return redirect("doctor:docApp")

    context['approve'] = approve
    return render(request, 'doctor/approveApp.html', context)  


@login_required(login_url='doctor:doctorLogin')
def reschedule(request, rs_id):
    context = {}
    appToReschedule = get_object_or_404(UserAppointment, id=rs_id)
    rescheduleForm = RescheduleForm(request.POST or None, instance=appToReschedule)

    if rescheduleForm.is_valid():
        rescheduleForm.save()
        messages.info(request, 'Approval was a success.')
        return redirect("doctor:docApp")

    context['rescheduleForm'] = rescheduleForm
    return render(request, 'doctor/reschedule.html', context)  



def aboutUsPage(request):
    context = {}
    return render(request, 'doctor/aboutUs.html', context)