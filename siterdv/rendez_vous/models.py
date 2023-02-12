from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from siterdv import settings



# Utilisateur = settings.AUTH_USER_MODEL

TIME_CHOICES = (
                        ("3 PM", "3 PM"),
                        ("3:30 PM", "3:30 PM"),
                        ("4 PM", "4 PM"),
                        ("4:30 PM", "4:30 PM"),
                        ("5 PM", "5 PM"),
                        ("5:30 PM", "5:30 PM"),
                        ("6 PM", "6 PM"),
                        ("6:30 PM", "6:30 PM"),
                        ("7 PM", "7 PM"),
                        ("7:30 PM", "7:30 PM"),
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
    user=models.ForeignKey(User,on_delete=models.CASCADE)
	


           

