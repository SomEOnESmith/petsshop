from django import forms
from .models import Pet
from django.contrib.auth.models import User


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ['available']

class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = '__all__'
    
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name' , 'last_name' , 'password']

        widgets = {
        	'password': forms.PasswordInput(),
        }

class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


