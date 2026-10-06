from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Resume, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=User.Role.choices)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["file"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "location",
            "headline",
            "experience_years",
            "profile_picture",
        ]
