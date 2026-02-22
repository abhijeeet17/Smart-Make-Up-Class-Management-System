from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone


class UserProfile(models.Model):
    """Extends User with role (faculty or student)"""
    ROLE_CHOICES = [
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    registration_number = models.CharField(max_length=20, blank=True, null=True)  # For students
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"

    def is_faculty(self):
        return self.role == 'faculty'

    def is_student(self):
        return self.role == 'student'


class MakeUpClass(models.Model):
    """A make-up/remedial class scheduled by faculty"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makeup_classes')
    subject = models.CharField(max_length=150)
    topic = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.subject} - {self.date} ({self.faculty.get_full_name()})"

    def get_active_code(self):
        """Returns the currently active remedial code for this class"""
        return self.remedial_codes.filter(is_active=True).first()

    def total_attendance(self):
        return MakeUpAttendance.objects.filter(makeup_class=self, is_present=True).count()


def generate_remedial_code():
    """Generate a unique 6-character alphanumeric code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class RemedialCode(models.Model):
    """Unique code generated per make-up class session"""
    makeup_class = models.ForeignKey(MakeUpClass, on_delete=models.CASCADE, related_name='remedial_codes')
    code = models.CharField(max_length=10, unique=True, default=generate_remedial_code)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Code: {self.code} | {self.makeup_class.subject}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        return self.is_active and not self.is_expired()

    def deactivate(self):
        self.is_active = False
        self.save()


class MakeUpAttendance(models.Model):
    """Attendance record for make-up classes — kept separate from regular attendance"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makeup_attendance')
    makeup_class = models.ForeignKey(MakeUpClass, on_delete=models.CASCADE, related_name='attendance_records')
    remedial_code_used = models.ForeignKey(RemedialCode, on_delete=models.SET_NULL, null=True, blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'makeup_class')
        ordering = ['-marked_at']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.get_full_name()} - {self.makeup_class.subject} - {status}"
