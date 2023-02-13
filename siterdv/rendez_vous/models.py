from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from siterdv import settings


utilisateurs = User.objects.values_list('id', 'username')
# Utilisateur = settings.AUTH_USER_MODEL

TIME_CHOICES = (
                        ("9 h", "9h"),
                        ("9h55", "9h55"),
                        ("10h50", "10h50"),
                        ("11h45", "11h45"),
                        ("13h30", "13h30"),
                        ("14h25", "14h25"),
                        ("15h20", "15h20"),
                        ("16h15", "16h15"),
            )

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)
   
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return f"{self.user} | day: {self.day} | time: {self.time}"




class Note(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
	
class Notes_associe_user(models.Model):
    nom = models.CharField(max_length=10, choices=utilisateurs)
    

           

