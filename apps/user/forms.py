from django import forms
from apps.user.models import User


class AcceptInvitationForm(forms.Form):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
