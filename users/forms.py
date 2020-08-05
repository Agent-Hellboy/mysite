from django import forms

from django.forms import ModelForm
from .models import User,Team
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "team"]

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["title", "description"]
