from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Case


class SignUpForm(UserCreationForm):
    """Signup Form inherited from django USERCreationForm model"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    personal_information = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['photo', 'personal_information']


class CaseForm(forms.ModelForm):

    class Meta:
        model = Case

        fields = ["title", "description", "comment", "date", "evidence", "number"]


class CreateCaseForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    number = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))
    evidence = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Case
        fields = ["title", "number", "date", "evidence"]


