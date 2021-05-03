from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import View
# from africasTalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

from .forms import *
from .models import *
from doctor.models import Doctor

# Create your views here.


def indexPage(request):
    context = {}
    return render(request, 'GTemp/index.html', context)


def RegPage(request):
    if request.user.is_authenticated:
        return redirect('mainApp:index')
    else:
        form = RegForm()
        if request.method == 'POST':
            form = RegForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account creation was successful.')
                return redirect('mainApp:login')
        else:
            form = RegForm()

        context = {'form': form}
        return render(request, 'authTemp/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('mainApp:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('mainApp:index')
            else:
                messages.info(request, 'Wrong Username or Password')

        context = {}
        return render(request, 'authTemp/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('mainApp:login')


# @login_required(login_url='authTemp/login.html')
def profilePage(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile creation was successful.')
            return redirect('mainApp:index')
    else:
        return redirect('mainApp:profile')

    context = {'form': form}
    return render(request, 'User/profile.html', context)


@login_required(login_url='authTemp/login.html')
def view_profile(request, user_id):
    profile = Profile.get_profile(user_id)
    context = {'profile': profile}
    return render(request, 'User/profileView.html', context)


@login_required(login_url='authTemp/login.html')
def all_questions(request):
    questions = Question.get_questions
    context = {'questions': questions}
    return render(request, 'GTemp/chatroom.html', context)


@login_required(login_url='authTemp/login.html')
def single_questions(request, question_id):
    questions = Question.objects.filter(id=question_id)
    comments = Comment.objects.filter(question=question_id)
    context = {'questions': questions, 'comments': comments}
    return render(request, 'GTemp/chatroom-q.html', context)


@login_required(login_url='authTemp/login.html')
def post_question(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.user = request.user
            opinion.save()
            return redirect('mainApp:chatroom')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'GTemp/addQuestion.html', context)


@login_required(login_url='authTemp/login.html')
def post_comments(request, question_id):
    current_question = Question.objects.get(id=question_id)
    print(current_question)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = current_question
            comment.save()
            # return redirect('chatroom', id=current_question.id)
            return HttpResponseRedirect(reverse('mainApp:chatroom')) 
    else:
        form = CommentForm()

    context = {'form': form, 'current_question': current_question}
    return render(request, 'GTemp/addComment.html', context)


@login_required(login_url='authTemp/login.html')
def appointment(request):
    user = request.user
    apps = UserAppointment.objects.filter(user=user.id)
    doctor = Doctor.objects.filter(availability=True)

    form = UserAppointmentForm()
    if request.method == 'POST':
        form = UserAppointmentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('mainApp:appointment')
    else:
        form = UserAppointmentForm()

    context = {'form': form, 'apps':apps, 'doctor':doctor}
    return render(request, 'GTemp/appointment.html', context)


@login_required(login_url='authTemp/login.html')
def view_records(request):
    profile = Record.get_records
    context = {'profile': profile}
    return render(request, 'authTemp/register.html', context)


@login_required(login_url='authTemp/login.html')
def unbooked_session(request):
    session = Session.get_questions
    context = {'session': session}
    return render(request, 'authTemp/register.html', context)


@login_required(login_url='authTemp/login.html')
def unbooked_vacancies(request):
    session = Inpatient.get_vacancies
    context = {'session': session}
    return render(request, 'authTemp/register.html', context)


@login_required(login_url='authTemp/login.html')
def view_outpatient(request):
    current_user = request.user
    reservations = Session.get_booked_sessions
    context = {'reservations': reservations, 'current_user': current_user}
    return render(request, 'view-out-booked.html', context)


@login_required(login_url='authTemp/login.html')
def view_inpatient(request):
    current_user = request.user
    reservations = Session.get_booked_sessions
    context = {'reservations': reservations, 'current_user': current_user}
    return render(request, 'view-in-booked.html', context)


# @login_required(login_url='authTemp/login.html')
# def reserve_session(request, session_id):
#     profile = Profile.get_profile(request.user.id)
#     user_contact = profile.phone
#     sessions = Session.object.get_sessions
#     session = Session.object.get(id=session_id)
#     session.Availability = False
#     session.user = request.user

#     when = session.session.slotted_date

#     # send confirmation massage to user
#     username = 'rehab'
#     apikey = '28394eac60fafaa60feb35012a8ddce5c5a5c164ba51a6f54d13c8f807daea543o'
#     to = user_contact
#     message = 'Hello' + request.user.username.upper() + \
#         '\nYou have successifully reserved a session with us'
#     gateway = AfricasTalkingGateway(username, apikey)

#     try:
#         results = gateway.sendMessage(to, message)

#         for recipient in results:
#             print('number=%s;status=%s;messageId=%s;cost=%s;' % (
#                 recipient['number'], recipient['status'], recipient['messageId'], recipient['cost']))

#     except AfricasTalkingGatewayException as e:
#         print('Encountered an error while sending: %s' % str(e))

#     return redirect('bookings')


# @login_required(login_url='authTemp/login.html')
# def inpatient_reservation(request, inpatient_id):
#     profile = Profile.get_profile(request.user.id)
#     user_contact = profile.phone
#     vacancies = Session.object.get_vacancies
#     vacancy = Session.object.get(id=inpatient_id)
#     vacancy.Availability = False
#     vacancy.save()

#     starting = vacancy.starting_date
#     ending = vacancy.finish_date

#     username = 'rehab'
#     apikey = '28394eac60fafaa60feb35012a8ddce5c5a5c164ba51a6f54d13c8f807daea543o'
#     to = user_contact
#     message = 'Congratulations' + request.user.username.upper() + '.\n' 'You have reserved a slot a iRehab from ' + \
#         str(starting)[:10] + 'to' + str(ending)[:10]

#     gateway = AfricasTalkingGateway(username, apikey)

#     try:
#         results = gateway.sendMessage(to, message)

#         for recipient in results:
#             print('number=%s;status=%s;messageId=%s;cost=%s;' % (
#                 recipient['number'], recipient['status'], recipient['messageId'], recipient['cost']))

#     except AfricasTalkingGatewayException as e:
#         print('Encountered an error while sending: %s' % str(e))

#     return redirect('bookings')
