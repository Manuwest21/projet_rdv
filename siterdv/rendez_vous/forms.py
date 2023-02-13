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
        
   # def clean_day(self):
   #      data = self.cleaned_data['day']
   #      today = date.today()
   #      limit = today + timedelta(days=60)
   #      if data < today or data > limit:
   #          raise ValidationError("La date doit être dans les 60 prochains jours.")
   #      if data.weekday() not in range(5):
   #          raise ValidationError("Les rendez-vous ne peuvent être pris que du lundi au vendredi.")
   #      return data

   # def clean(self):
   #      cleaned_data = super().clean()
   #      day = cleaned_data.get("day")
   #      time = cleaned_data.get("time")
   #      if day and time:
   #          existing_appointment = Appointment.objects.filter(day=day, time=time)
   #          if existing_appointment.exists():
   #              raise ValidationError("Il y a déjà un rendez-vous à cette heure et date.")
        
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
   # email = forms.EmailField()
   username= forms.CharField(max_length=1000)   
    
    
    # discord_id = forms.CharField(max_length=100, help_text='Discord ID')
    # zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')