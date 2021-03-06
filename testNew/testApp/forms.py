from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateField


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}

from django import forms

from django.contrib.auth.models import User
from .models import Profile , Case


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


# creating a form
class CaseForm(forms.ModelForm):


    class Meta:
        # specify model to be used
        model = Case

        # specify fields to be used
        fields = ["title", "description", "comment", "date", "FIR", "number"]
        #fields = ["title", "number", "date", "FIR"]

class CreateCaseForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    number = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    date= forms.DateField(widget= forms.DateInput(format='%d/%m/%Y'))
    FIR = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))


    class Meta:
        model = Case
        fields = ["title", "number", "date", "FIR"]


