from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MakeUpClass, UserProfile
from django.utils import timezone
from datetime import timedelta


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [('student', 'Student'), ('faculty', 'Faculty')]
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    registration_number = forms.CharField(max_length=20, required=False, help_text="Required for students (e.g. 12215454)")
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        reg_no = cleaned_data.get('registration_number')
        if role == 'student' and not reg_no:
            self.add_error('registration_number', 'Registration number is required for students.')
        return cleaned_data


class MakeUpClassForm(forms.ModelForm):
    class Meta:
        model = MakeUpClass
        fields = ['subject', 'topic', 'date', 'start_time', 'end_time', 'venue', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and start >= end:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data


class RemedialCodeForm(forms.Form):
    """Form for faculty to generate a remedial code with expiry"""
    DURATION_CHOICES = [
        (15, '15 minutes'),
        (30, '30 minutes'),
        (60, '1 hour'),
        (120, '2 hours'),
    ]
    duration_minutes = forms.ChoiceField(
        choices=DURATION_CHOICES,
        label="Code valid for",
        initial=30,
    )


class AttendanceMarkForm(forms.Form):
    """Form for student to enter remedial code"""
    code = forms.CharField(
        max_length=10,
        label="Enter Remedial Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. AB1C2D',
            'class': 'code-input',
            'autocomplete': 'off',
            'style': 'text-transform: uppercase; letter-spacing: 4px; font-size: 1.4rem;'
        })
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()
