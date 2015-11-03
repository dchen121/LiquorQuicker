from django import forms
from .models import LQUser

class SignUpForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = LQUser
		fields = ('username','screen_name', 'password','avatar')