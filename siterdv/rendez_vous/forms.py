from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Appointment, Note, Notes_associe_user
from django.forms import ModelForm
from datetime import timedelta, date
from django.core.exceptions import ValidationError






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
        
 
class Formu_note_users(ModelForm):
   
   class Meta:
        model = Notes_associe_user
        fields = [ "nom"]    
        
class Formu_note(ModelForm):
   
   class Meta:
        model = Note
        fields = [ "title", "content","client"]
        
class LoginForm(AuthenticationForm):
    username= forms.CharField 
    
    
class add_note(forms.Form):
   name = forms.CharField(required=False, widget=forms.TextInput(
      attrs={
         'placeholder':'votre nom ici'
      }
   ))
  
   username= forms.CharField(max_length=1000)   
    
    
    