from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Moderator

class ContentStatus(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput)
    status = forms.CharField()

class Login(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class Create(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())



class ModeratorCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Moderator
        fields = ('email',)


class ModeratorChangeForm(UserChangeForm):

    class Meta:
        model = Moderator
        fields = ('email',)