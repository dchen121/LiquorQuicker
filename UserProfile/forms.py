from django import forms
from .models import LQUser


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LQUser
        fields = ('username', 'password', 'first_name', 'last_name', 'avatar')
