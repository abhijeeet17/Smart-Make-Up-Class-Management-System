from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Faculty
    path('classes/', views.faculty_classes, name='faculty_classes'),
    path('classes/schedule/', views.schedule_class, name='schedule_class'),
    path('classes/<int:pk>/', views.class_detail, name='class_detail'),
    path('classes/<int:pk>/edit/', views.edit_class, name='edit_class'),
    path('classes/<int:pk>/delete/', views.delete_class, name='delete_class'),

    # Student
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/my/', views.my_attendance, name='my_attendance'),

    # AJAX
    path('api/code/<int:pk>/status/', views.check_code_status, name='check_code_status'),
]
