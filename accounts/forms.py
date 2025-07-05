from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].error_messages = {'unique': 'This phone number is already registered.'}


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password')
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder':'Enter username'}),
            'password' : forms.PasswordInput(attrs={'placeholder':'Enter username'})
        }

class identifyForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Enter your username"
    )
