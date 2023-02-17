from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rendez_vous.forms import RegisterForm,Rendez, Formu_note, Formu_note_users
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rendez_vous.models import Note
from datetime import timedelta
import datetime
from django.views.generic import View
from.models import Appointment, User
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError

def home (request):
    return render (request, 'rendez_vous/home.html')

@login_required
def home(request):
	context ={
	'notes': Note.objects.all()
	}
	return render(request, 'rendez_vous/home.html',context)


@staff_member_required
def add_note(request):
    if request.method=='POST':
        note=Note(request.POST)
    else:
        note=Note(request.POST)
    return render (request, "rendez_vous/add_note.html", {'note':note})

def a_mon_propos(request):
    return render (request, "rendez_vous/a_mon_propos.html")

def methode_coaching(request):
    return render (request, "rendez_vous/methode_coaching.html")



def register(request):
    if request.method == 'POST':               #check si l'user veut envoyer des données
        form = RegisterForm(request.POST)      #si oui, on crée une instance de la classe userform _ avec méthode post(pr laissr entrer des valeurs)  >>> on le met ds une variable appelée 'form'
        if form.is_valid():                    #on vérifie si le form est valide   >>> si oui  : on le sauvegarde
            form.save()
                  
            user= form.cleaned_data.get('username')
            messages.success(request, "votre compte est magnifiquement créé!" + user)
            return redirect('login_p')        #on fait une redirection vers une page x
    else:
        form = RegisterForm()                 #autrement, si la requête est pas un post, on met juste une instance vide de RegisterForm

    return render (request, "rendez_vous/register.html", {'form':form})







def confirmation_rdv(request):                                          # page d'information du confirmation de rdv, uniquement quand le rdv est sauvegardé
  
    return render (request, 'rendez_vous/confirmation_rdv.html')





@login_required
def rdv(request):
    today = timezone.now().date()                                           #reprend la date du jour
    max_day = today + datetime.timedelta(days=60)                           #correspond à la date du jour + une date définie à j+60 (le coach n'accepte pas de prise de rendez-vous plus de 2 mois à l'avance)
    day=today
  
    if request.method == 'POST':
        form = Rendez(request.POST)
        if form.is_valid():
            appointment=form.save(commit=False)
            appointment.user = request.user
            day = appointment.day                                                      #date du jour de la prise de rendez-vous par le client
            time = appointment.time
            if day < today or day > max_day:                                           #si la date sélectionnée est dans le passé ou supérieur à la date de +60jours
                messages.error(request, "Le jour sélectionné n'est pas disponible pour une réservation, je ne propose pas de réservation de rendez-vous au delà des 60 prochains jours")
                return redirect('reserver')                                            #on reste sur la page avec message d'erreur qui s'affiche dessus 
            if day.weekday() >= 5:                                                     #si le jour sélectionné est un samedi ou dimanche: message d'erreur pour dire que la prise de rdv n'a lieu qu'en semaine
                messages.error(request, "Les rendez-vous ne sont disponibles que du lundi au vendredi")
                return redirect('reserver')
            existing_appointments = Appointment.objects.filter(day=day, time=time)     #reprend tous les champs jour et heure des "objets" appointement
            if existing_appointments.exists():                                         #si la date et heure sélectionnée correspondent à un rdv déjà pris: message d'erreur et pas d'enregistrement rdv
                messages.error(request, "Il existe déjà un rendez-vous à cette date et à cette heure")
                return redirect('reserver')
            appointment.save()                                                          #si tous les critères sont remplis: enregistrement du rdv
            messages.success(request, "Votre rendez-vous a été créé avec succès!")
            return redirect('confirmation_rdv')                                         #renvoi vers une page de confirmation du rdv
        else:
            print("Le formulaire est mal rempli, il y a des erreurs:", form.errors)     #affiche erreur si formulaire mal rempli
    else:
        appointment = Rendez()
        print("le rendez_vous est créé:", appointment)
    return render(request, 'rendez_vous/reserver.html', {'form': appointment, 'messages': messages.get_messages(request),'day':day,'today':today,'max_day':max_day})

def mes_rdv(request):                                                                   #reprend les "objets" rdv, en filtrant ceux correpondant à l'utilisateur connecté
    appointments = Appointment.objects.filter(user=request.user).order_by('day','time') #les rdv sont triés par ordre chronologique 
    return render(request, 'rendez_vous/mes_rdv.html', {'appointments': appointments})

def list_all_rdv(request):                                                              #cf 'base.html'( {% if user.is_authenticated %})>> seul les users définis comme 'staff', donc le coach, ont accés à cet onglet de page
    appointments = Appointment.objects.all().order_by('day','time')                     #répertorie tous les rdv, triés chronologiquement
    return render(request, 'rendez_vous/list_all_rdv.html', {'appointments': appointments})

def add_note(request, nom_user_rdv):                                                    #donne la possibilité d'ajouter une note, fonctionalité disponible à partir de la liste de tous les rendez_vous
   
    user=nom_user_rdv
    if request.method == 'POST':
        form = Formu_note(request.POST)
        if form.is_valid():
            form.cleaned_data['client'] = user                                         #la note est assignée au client pour lequel le coach veut ajouter une note
            form.save()
            return redirect('list_all_rdv')
    else:
        form = Formu_note()
    return render(request, 'rendez_vous/add_note.html', {'form': form, 'client':user})



def notes_ciblees(request, nom_client):                                                                  #page qui renvoyée à partir de "note_user", va afficher les notes déjà écrites concernant le client sélectionné
                                                                                                         #"nom_client" correspond au nom du client pour lequel on veut accéder aux notes
    users = User.objects.filter(username=nom_client)                                                     #va reprendre le client qui est associé à ce nom
    if users.exists():
        client = users.first().id                                                                        #à partir du nom du client, on reprend son id
        notes = Note.objects.all().filter(client=client)                                                 #on accéde aux notes uniquement correpondantantes au client sélectionné
    else:
        notes = []
    return render(request, 'rendez_vous/notes_ciblees.html',{'nom_client':nom_client, 'notes':notes})    #renvoi du nom du client et ses notes à la page html

def note_user(request):
    user=User.objects.all()
    
    if request.method == 'POST':         
        form = Formu_note_users(request.POST)                   #le formulaire permet de chosiir le client pour lequel on veut ajouter une note
        if form.is_valid():                                     #on vérifie si le form est valide   >>> si oui  : on le sauvegarde
            form.save(commit=False)
            user=form.cleaned_data['nom'] 
            form.save()
           
    else:
        form = Formu_note_users()                 
    return render (request, "rendez_vous/note_user.html", {'form':form, 'user':user})   #renvoi du nom client et du formulaire
            

def liste_rdv(request):
    rdv=Appointment.objects.all()
    return render (request, "rendez_vous/liste_rdv.html", {'form':rdv})

def login_p(request):
    if request.method== "POST":
        form= AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form= AuthenticationForm(request)
        
    
    return render (request, "rendez_vous/login_p.html", {'form':form})

def loggout(request):
    if request.method== "POST":
        logout(request)
        return redirect ('login')
    else:
        form=logout(request)
    return render (request, "rendez_vous/loggout.html", {'form':form})



