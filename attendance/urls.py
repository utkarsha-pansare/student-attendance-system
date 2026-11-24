
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('login/', auth_views.LoginView.as_view(template_name='attendance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('home/', views.home, name='home'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('defaulters/', views.defaulters, name='defaulters'),
    path('send-alerts/', views.send_alerts, name='send_alerts'),
]