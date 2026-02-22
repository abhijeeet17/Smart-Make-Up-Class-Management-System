from django.contrib import admin
from .models import UserProfile, MakeUpClass, RemedialCode, MakeUpAttendance


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'registration_number', 'department']
    list_filter = ['role']
    search_fields = ['user__username', 'user__first_name', 'registration_number']


@admin.register(MakeUpClass)
class MakeUpClassAdmin(admin.ModelAdmin):
    list_display = ['subject', 'faculty', 'date', 'start_time', 'venue', 'status']
    list_filter = ['status', 'date']
    search_fields = ['subject', 'faculty__first_name']


@admin.register(RemedialCode)
class RemedialCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'makeup_class', 'is_active', 'created_at', 'expires_at']
    list_filter = ['is_active']


@admin.register(MakeUpAttendance)
class MakeUpAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'makeup_class', 'is_present', 'marked_at']
    list_filter = ['is_present', 'marked_at']
    search_fields = ['student__first_name', 'student__username']
