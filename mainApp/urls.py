from mainApp.models import Profile
from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
    path('', views.indexPage, name='index'),

    path('auth/register/', views.RegPage, name='register'),
    path('auth/login/', views.loginPage, name='login'),
    path('auth/logout/', views.logoutPage, name='logout'),

    path('profile/<int:uid>/', views.profilePage, name='profile'),
    # path('profile/', views.view_profile, name='viewProfile'),

    path('chatroom/', views.all_questions, name='chatroom'),
    path('chartroom/<int:question_id>/question', views.single_questions, name='question'),
    path('chartroom/ask-question', views.post_question, name='askQuiz'),

    path('chartroom/<int:question_id>/question/add_comment',
         views.post_comments, name='add_comment'),
    #     path('chartroom/<int:q_pk/question/<int:c_pk/comment', views.)

    path('appointment/bookings/', views.appointment, name="appointment"),

    path('About_us/', views.aboutPage, name="aboutPage")
]
