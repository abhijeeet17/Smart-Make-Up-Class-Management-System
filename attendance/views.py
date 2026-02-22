from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

from .models import MakeUpClass, RemedialCode, MakeUpAttendance, UserProfile
from .forms import RegisterForm, MakeUpClassForm, RemedialCodeForm, AttendanceMarkForm


# ──────────────────────────────────────────────
#  Auth Views
# ──────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                registration_number=form.cleaned_data.get('registration_number', ''),
                department=form.cleaned_data.get('department', ''),
            )
            login(request, user)
            messages.success(request, f"Welcome to LPU Campus, {user.first_name}!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'attendance/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'attendance/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ──────────────────────────────────────────────
#  Dashboard
# ──────────────────────────────────────────────

@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    if not profile:
        messages.warning(request, "Please complete your profile setup.")
        return redirect('login')

    if profile.is_faculty():
        classes = MakeUpClass.objects.filter(faculty=request.user).order_by('-date')[:5]
        total_classes = MakeUpClass.objects.filter(faculty=request.user).count()
        active_codes = RemedialCode.objects.filter(
            created_by=request.user, is_active=True
        ).select_related('makeup_class')
        context = {
            'classes': classes,
            'total_classes': total_classes,
            'active_codes': active_codes,
            'role': 'faculty',
        }
    else:
        attended = MakeUpAttendance.objects.filter(
            student=request.user, is_present=True
        ).select_related('makeup_class').order_by('-marked_at')[:5]
        total_attended = MakeUpAttendance.objects.filter(student=request.user, is_present=True).count()
        context = {
            'attended': attended,
            'total_attended': total_attended,
            'role': 'student',
        }

    return render(request, 'attendance/dashboard.html', context)


# ──────────────────────────────────────────────
#  Faculty: Manage Make-Up Classes
# ──────────────────────────────────────────────

@login_required
def schedule_class(request):
    """Faculty: schedule a new make-up class"""
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_faculty():
        messages.error(request, "Only faculty can schedule make-up classes.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = MakeUpClassForm(request.POST)
        if form.is_valid():
            cls = form.save(commit=False)
            cls.faculty = request.user
            cls.save()
            messages.success(request, f"Make-up class for '{cls.subject}' scheduled successfully!")
            return redirect('class_detail', pk=cls.pk)
    else:
        form = MakeUpClassForm()
    return render(request, 'attendance/schedule_class.html', {'form': form})


@login_required
def faculty_classes(request):
    """Faculty: list all their make-up classes"""
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_faculty():
        return redirect('dashboard')
    classes = MakeUpClass.objects.filter(faculty=request.user).order_by('-date')
    return render(request, 'attendance/faculty_classes.html', {'classes': classes})


@login_required
def class_detail(request, pk):
    """Faculty: detail view for a make-up class, generate code, see attendance"""
    cls = get_object_or_404(MakeUpClass, pk=pk)
    profile = get_object_or_404(UserProfile, user=request.user)

    # Only faculty who owns the class or any student can see it
    if profile.is_faculty() and cls.faculty != request.user:
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    attendance_records = MakeUpAttendance.objects.filter(
        makeup_class=cls
    ).select_related('student').order_by('-marked_at')

    active_code = cls.get_active_code()
    code_form = RemedialCodeForm()

    if request.method == 'POST' and profile.is_faculty():
        action = request.POST.get('action')

        if action == 'generate_code':
            code_form = RemedialCodeForm(request.POST)
            if code_form.is_valid():
                # Deactivate old codes
                cls.remedial_codes.filter(is_active=True).update(is_active=False)
                duration = int(code_form.cleaned_data['duration_minutes'])
                RemedialCode.objects.create(
                    makeup_class=cls,
                    created_by=request.user,
                    expires_at=timezone.now() + timedelta(minutes=duration),
                    is_active=True,
                )
                messages.success(request, "New remedial code generated!")
                return redirect('class_detail', pk=pk)

        elif action == 'deactivate_code':
            cls.remedial_codes.filter(is_active=True).update(is_active=False)
            messages.info(request, "Remedial code deactivated.")
            return redirect('class_detail', pk=pk)

        elif action == 'activate_class':
            cls.status = 'active'
            cls.save()
            return redirect('class_detail', pk=pk)

        elif action == 'complete_class':
            cls.status = 'completed'
            cls.remedial_codes.filter(is_active=True).update(is_active=False)
            cls.save()
            messages.success(request, "Class marked as completed.")
            return redirect('class_detail', pk=pk)

    context = {
        'cls': cls,
        'attendance_records': attendance_records,
        'active_code': active_code,
        'code_form': code_form,
        'role': profile.role,
    }
    return render(request, 'attendance/class_detail.html', context)


@login_required
def edit_class(request, pk):
    cls = get_object_or_404(MakeUpClass, pk=pk, faculty=request.user)
    if request.method == 'POST':
        form = MakeUpClassForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated.")
            return redirect('class_detail', pk=pk)
    else:
        form = MakeUpClassForm(instance=cls)
    return render(request, 'attendance/schedule_class.html', {'form': form, 'editing': True})


@login_required
def delete_class(request, pk):
    cls = get_object_or_404(MakeUpClass, pk=pk, faculty=request.user)
    if request.method == 'POST':
        cls.delete()
        messages.success(request, "Make-up class deleted.")
        return redirect('faculty_classes')
    return render(request, 'attendance/confirm_delete.html', {'cls': cls})


# ──────────────────────────────────────────────
#  Student: Mark Attendance
# ──────────────────────────────────────────────

@login_required
def mark_attendance(request):
    """Student: enter remedial code to mark attendance"""
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_student():
        messages.error(request, "Only students can mark attendance.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = AttendanceMarkForm(request.POST)
        if form.is_valid():
            code_str = form.cleaned_data['code']
            try:
                code_obj = RemedialCode.objects.select_related('makeup_class').get(code=code_str)
            except RemedialCode.DoesNotExist:
                messages.error(request, f"Code '{code_str}' is not valid. Please check and try again.")
                return render(request, 'attendance/mark_attendance.html', {'form': form})

            if not code_obj.is_valid():
                messages.error(request, "This code has expired or been deactivated. Ask your faculty for a new code.")
                return render(request, 'attendance/mark_attendance.html', {'form': form})

            cls = code_obj.makeup_class
            # Check duplicate
            if MakeUpAttendance.objects.filter(student=request.user, makeup_class=cls).exists():
                messages.warning(request, f"You have already marked attendance for '{cls.subject}'.")
                return redirect('my_attendance')

            MakeUpAttendance.objects.create(
                student=request.user,
                makeup_class=cls,
                remedial_code_used=code_obj,
                is_present=True,
            )
            messages.success(request, f"✅ Attendance marked for '{cls.subject}' on {cls.date}!")
            return redirect('my_attendance')
    else:
        form = AttendanceMarkForm()

    return render(request, 'attendance/mark_attendance.html', {'form': form})


@login_required
def my_attendance(request):
    """Student: view their own make-up class attendance records"""
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_student():
        return redirect('dashboard')

    records = MakeUpAttendance.objects.filter(
        student=request.user
    ).select_related('makeup_class', 'makeup_class__faculty').order_by('-marked_at')

    return render(request, 'attendance/my_attendance.html', {
        'records': records,
        'total': records.count(),
    })


# ──────────────────────────────────────────────
#  AJAX: Code Status Check
# ──────────────────────────────────────────────

@login_required
def check_code_status(request, pk):
    """AJAX endpoint to check if active code still valid"""
    try:
        code = RemedialCode.objects.get(pk=pk)
        return JsonResponse({
            'is_valid': code.is_valid(),
            'expires_at': code.expires_at.isoformat(),
            'time_left': max(0, int((code.expires_at - timezone.now()).total_seconds())),
        })
    except RemedialCode.DoesNotExist:
        return JsonResponse({'is_valid': False})
