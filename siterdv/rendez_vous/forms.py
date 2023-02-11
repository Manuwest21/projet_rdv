from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Appointment
from django.forms import ModelForm

class RegisterForm(UserCreationForm):
    birthdate = forms.DateField()
    
    email= forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "birthdate", "email"]


class Rendez(ModelForm):
   
   class Meta:
        model = Appointment
        fields = [ "day", "time_ordered", "time"]
        
class LoginForm(AuthenticationForm):
    username= forms.CharField 
    
    
class add_note(forms.Form):
   name = forms.CharField(required=False, widget=forms.TextInput(
      attrs={
         'placeholder':'votre nom ici'
      }
   ))
   # email = forms.EmailField()
   username= forms.CharField(max_length=1000)   
    
    
    # discord_id = forms.CharField(max_length=100, help_text='Discord ID')
    # zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')