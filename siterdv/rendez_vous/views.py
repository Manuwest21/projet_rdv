from django.shortcuts import render, redirect
from django.http import HttpResponse
# from testy.forms import ContactUsForm, EtudiantForm
# from testy.register import UserForm
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




def register(request):
    if request.method == 'POST':          #check si l'user veut envoyer des données
        form = RegisterForm(request.POST)     #si oui, on crée une instance de la classe userform _ avec méthode post(pr laissr entrer des valeurs)  >>> on le met ds une variable appelée 'form'
        if form.is_valid():               #on vérifie si le form est valide   >>> si oui  : on le sauvegarde
            form.save()
                  #on fait une redirection vers une page x
            user= form.cleaned_data.get('username')
            messages.success(request, "votre compte est magnifiquement créé!" + user)
            return redirect('login_p') 
    else:
        form = RegisterForm()                 #However, if the request is not a POST request, we just create an instance of the empty UserForm. 

    return render (request, "rendez_vous/register.html", {'form':form})




# @login_required
# def rdv(request):
#     if request.method == 'POST':
#         form = Rendez(request.POST)     
#         if form.is_valid():
#             appointment=form.save(commit=False)
#             appointment.user = request.user
#             appointment.save()
#             messages.success(request, "votre rdv est magnifiquement créé!")
#             return redirect('login_p') 
#     else:
#         form = Rendez(initial={'user': request.user})
#     return render(request, 'rendez_vous/reserver.html', {'form': form})

# @login_required
# def rdv(request):
#     if request.method == 'POST':
#         form = Rendez(request.POST)     
#         if form.is_valid():
#             appointment=form.save(commit=False)
#             appointment.user = request.user
#             appointment.save()
#             messages.success(request, "votre rdv est magnifiquement créé!")
#             return redirect('login_p') 
#     else:
#         form = Rendez()
        
#     return render(request, 'rendez_vous/reserver.html', {'form': form})
# @login_required
# def rdv(request):
#     if request.method == 'POST':
#         form = Rendez(request.POST)     
#         if form.is_valid():
#             appointment=form.save(commit=False)
#             appointment.user = request.user
#             form.save()
#             # appointment.save()
#             messages.success(request, "votre rdv est magnifiquement créé!")
#             return redirect('confirmation_rdv')                         
#         else:
#             messages.error(request,"Le formulaire est mal rempli, il y a des erreurs:")
#     else:
#         form = Rendez()
#         # print("le rendez-vous a été créé", appointment)
        
#     return render(request, 'rendez_vous/reserver.html', {'form': form})

# @login_required
# def rdv(request):
#     if request.method == 'POST':
#         form = Rendez(request.POST)     
#         if form.is_valid():
#             appointment=form.save(commit=False)
#             appointment.user = request.user
#             appointment.save()
#             messages.success(request, "votre rdv est magnifiquement créé!")
#             return redirect('confirmation_rdv')
#         else:
#             messages.error(request, "Le formulaire est mal rempli, veuillez corriger les erreurs.")
#     else:
#         form = Rendez()
        
#     return render(request, 'rendez_vous/reserver.html', {'form': form})


def confirmation_rdv(request):                                                          # page d'information du confirmation de rdv, uniquement quand le rdv est sauvegardé
   # appoint = Rendez.objects.get(id=id)
    return render (request, 'rendez_vous/confirmation_rdv.html')#{'appoint': appoint})


#def confirmation_rdv(request,id):  
    appoint = Rendez.objects.get(id=id)
    return render (request, 'rendez_vous/confirmation_rdv.html',{'appoint': appoint})


@login_required
def rdv(request):
    today = timezone.now().date()                                           #reprend la date du jour
    max_day = today + datetime.timedelta(days=60)                           #correspond à la date du jour + une date définie à j+60 (le coach n'accepte pas de prise de rendez-vous plus de 2 mois à l'avance)
    day=today
    # appointment=Rendez()
    if request.method == 'POST':
        form = Rendez(request.POST)
        if form.is_valid():
            appointment=form.save(commit=False)
            appointment.user = request.user
            day = appointment.day                                           #date du jour de la prise de rendez-vous par le client
            time = appointment.time
            if day < today or day > max_day:                                #si la date sélectionnée est dans le passé ou supérieur à la date de +60jours
                messages.error(request, "Le jour sélectionné n'est pas disponible pour une réservation, je ne propose pas de réservation de rendez-vous au delà des 60 prochains jours")
                return redirect('reserver')                                 #on reste sur la page avec message d'erreur qui s'affiche dessus 
            if day.weekday() >= 5:                                          #si le jour sélectionné est un samedi ou dimanche: message d'erreur pour dire que la prise de rdv n'a lieu qu'en semaine
                messages.error(request, "Les rendez-vous ne sont disponibles que du lundi au vendredi")
                return redirect('reserver')
            existing_appointments = Appointment.objects.filter(day=day, time=time)    #reprend tous les champs jour et heure des "objets" appointement
            if existing_appointments.exists():                                        #si la date et heure sélectionnée correspondent à un rdv déjà pris: message d'erreur et pas d'enregistrement rdv
                messages.error(request, "Il existe déjà un rendez-vous à cette date et à cette heure")
                return redirect('reserver')
            appointment.save()                                              #si tous les critères sont remplis: enregistrement du rdv
            messages.success(request, "Votre rendez-vous a été créé avec succès!")
            return redirect('confirmation_rdv')                             #renvoi vers une page de confirmation du rdv
        else:
            print("Le formulaire est mal rempli, il y a des erreurs:", form.errors)  #affiche erreur si formulaire mal rempli
    else:
        appointment = Rendez()
        print("le rendez_vous est créé:", appointment)
    return render(request, 'rendez_vous/reserver.html', {'form': appointment, 'messages': messages.get_messages(request),'day':day,'today':today,'max_day':max_day})

def mes_rdv(request):                                              #reprend les "objets" rdv, en filtrant ceux correpondant à l'utilisateur connecté
    appointments = Appointment.objects.filter(user=request.user).order_by('day','time')   #les rdv sont triés par ordre chronologique 
    return render(request, 'rendez_vous/mes_rdv.html', {'appointments': appointments})

def list_all_rdv(request):                                         #cf 'base.html'>> seul les users définis comme 'staff', donc le coach, a accés à cet onglet de page
    appointments = Appointment.objects.all().order_by('day','time') #répertorie tous les rdv, triés chronologiquement
    return render(request, 'rendez_vous/list_all_rdv.html', {'appointments': appointments})

def add_note(request, nom_user_rdv):                             #donne la possibilité d'ajouter une note, fonctionalité disponible à partir de la liste de tous les rendez_vous
    # user_x= nom_user_rdv                                       #la fonction reprend en paramétre le nom du client pour lequel on veut ajouter une note
    # user=rdv_x.user
    # user = User.objects.get(id=nom_user_rdv)
    user=nom_user_rdv
    if request.method == 'POST':
        form = Formu_note(request.POST)
        if form.is_valid():
            form.cleaned_data['client'] = user                   #la note est assignée au client pour lequel le coach veut ajouter une note
            form.save()
            # # note.user = nom_user_rdv
            # note.save()
            return redirect('list_all_rdv')
    else:
        form = Formu_note()
    return render(request, 'rendez_vous/add_note.html', {'form': form, 'client':user})

# def add_note(request, nom_user_rdv):
#     rdv_x= Appointment.objects.get(id=id)
#     user=rdv_x.user
#     user = User.objects.get(id=id_rdv)
#     if request.method == 'POST':
#         form = Formu_note(request.POST)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = user
#             note.save()
#             return redirect('list_all_rdv')
#     else:
#         form = Formu_note()
#     return render(request, 'rendez_vous/add_note.html', {'form': form})

# def note_user(request):
#     user = User.objects.all()
#     return render(request, 'rendez_vous/note_user.html',{'users':user})

def notes_ciblees(request, nom_client):                           #page qui renvoyée à partir de "note_user", va afficher les notes déjà écrites concernant le client sélectionné
    # user = User.objects.get(username=nom_client)                #"nom_client" correspond au nom du client pour lequel on veut accéder aux notes
    # client=user.id
    # # notes=Note.objects.all()S
    # notes = Note.objects.all().filter(client=nom_client)
    users = User.objects.filter(username=nom_client)             #va reprendre le client qui est associé à ce nom
    if users.exists():
        client = users.first().id                                #à partir du nom du client, on reprend son id
        notes = Note.objects.all().filter(client=client)         #on accéde aux notes uniquement correpondantantes au client sélectionné
    else:
        notes = []
    return render(request, 'rendez_vous/notes_ciblees.html',{'nom_client':nom_client, 'notes':notes})   #renvoi du nom du client et ses notes à la page html

def note_user(request):
    user=User.objects.all()
    
    if request.method == 'POST':         
        form = Formu_note_users(request.POST)                   #le formulaire permet de chosiir le client pour lequel on veut ajouter une note
        if form.is_valid():               #on vérifie si le form est valide   >>> si oui  : on le sauvegarde
            form.save(commit=False)
            user=form.cleaned_data['nom'] 
            form.save()
           # return redirect('home') 
    else:
        form = Formu_note_users()                 #However, if the request is not a POST request, we just create an instance of the empty UserForm. 

    return render (request, "rendez_vous/note_user.html", {'form':form, 'user':user})   #renvoi du nom client et du formulaire
            
# def add_note(request, id):
#     user = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = Formu_note(request.POST)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = user
#             note.save()
#             return redirect('list_all_rdv')
#     else:
#         form = Formu_note()
#     return render(request, 'rendez_vous/add_note.html', {'form': form})

# def add_note(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     form = Formu_note(request.POST or None)
#     if form.is_valid():
#         note = form.save(commit=False)
#         note.user = user
#         note.save()
#         return redirect('list_all_rdv')
#     return render(request, 'rendez_vous/add_note.html', {'form': form})
# def add_note(request, pk):
#     user = User.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = Formu_note(request.POST)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = user
#             note.save()
#             return redirect('list_all_rdv')
#     else:
#         form = Formu_note()
#     return render(request, 'rendez_vous/add_note.html', {'form': form})




# class LoginPageView(View):
#     template_name = 'authentication/login.html'
#     form_class = forms.LoginForm

#     def get(self, request):
#         form = self.form_class()
#         message = ''
#         return render(request, self.template_name, context={'form': form, 'message': message})
        
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#         message = 'Identifiants invalides.'
#         return render(request, self.template_name, context={'form': form, 'message': message})

# def confirmation_rdv(request):    
#     # if request.method == 'POST':
#     #     form = BandForm(request.POST)
#     #     if form.is_valid():
#     #         # créer une nouvelle « Band » et la sauvegarder dans la db
#     #         band = form.save()
#             # redirige vers la page de détail du groupe que nous venons de créer
#             # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
#             return render(request,'confirmation_rdv.html')

#     else:
#         form = BandForm()

#     return render(request,
#             'listings/band_create.html',
#             {'form': form})

# @login_required
# def rdv(request):
#     if request.method == 'POST':
#         form = Rendez(request.POST)     
#         if form.is_valid():
#             appointment=form.save(commit=False)
#             appointment.user = request.user
#             appointment.save()
#             messages.success(request, "votre rdv est magnifiquement créé!")
#             return redirect('login_p') 
#     else:
#         appointment = Rendez()
        
#     return render(request, 'rendez_vous/reserver.html', {'form': appointment})


# if form.is_valid():
#     instance = form.save(commit=False)
#     instance.user = request.user
#     instance.save()
# @login_required
# def rdv(request):
#     form=Rendez
#     if request.method == 'POST':         
#         appointment.user=request.user
#         form = Rendez(request.POST, user=request.user)     
#         if form.is_valid():               
#             appointment=form.save(commit=False)
#             appointment.save()
#             user= form.cleaned_data.get('username')
#             messages.success(request, "votre rdv est magnifiquement créé!" + user)
#             return redirect('login_p') 
#     else:
#         form = Rendez()                

#     return render (request, "rendez_vous/reserver.html", {'form':form})

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

@login_required
def profil_perso(request):
    return render (request, "rendez_vous/profil_perso.html")



def index(request):
    return render(request, "index.html",{})

# def reserver(request):
#     #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
#     weekdays = validWeekday(22)

#     #Only show the days that are not full:
#     validateWeekdays = isWeekdayValid(weekdays)
    

#     if request.method == 'POST':
#         # service = request.POST.get('service')
#         day = request.POST.get('day')
#         # if service == None:
#         #     messages.success(request, "Please Select A Service!")
#         #     return redirect('booking')

#         #Store day and service in django session:
#         request.session['day'] = day
#         # request.session['service'] = service

#         return redirect('bookingSubmit')


#     return render(request, 'reserver.html', {
#             'weekdays':weekdays,
#             'validateWeekdays':validateWeekdays,
#         })


# def bookingSubmit(request):
#     user = request.user
#     times = [
#         "9 AM", "9:55 AM", "10:50 AM", "11:45 AM", "13:30 PM", "14:25 PM", "15:20 PM", "16:15 PM"
#     ]
#     today = datetime.now()
#     minDate = today.strftime('%Y-%m-%d')
#     deltatime = today + timedelta(days=21)
#     strdeltatime = deltatime.strftime('%Y-%m-%d')
#     maxDate = strdeltatime

#     #Get stored data from django session:
#     day = request.session.get('day')
#     # service = request.session.get('service')
    
#     #Only show the time of the day that has not been selected before:
#     hour = checkTime(times, day)
#     if request.method == 'POST':
#         time = request.POST.get("time")
#         date = dayToWeekday(day)

#         if service != None:
#             if day <= maxDate and day >= minDate:
#                 if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
#                     if Appointment.objects.filter(day=day).count() < 11:
#                         if Appointment.objects.filter(day=day, time=time).count() < 1:
#                             AppointmentForm = Appointment.objects.get_or_create(
#                                 user = user,
#                                 service = service,
#                                 day = day,
#                                 time = time,
#                             )
#                             messages.success(request, "Appointment Saved!")
#                             return redirect('index')
#                         else:
#                             messages.success(request, "The Selected Time Has Been Reserved Before!")
#                     else:
#                         messages.success(request, "The Selected Day Is Full!")
#                 else:
#                     messages.success(request, "The Selected Date Is Incorrect")
#             else:
#                     messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
#         else:
#             messages.success(request, "Please Select A Service!")


#     return render(request, 'bookingSubmit.html', {
#         'times':hour,
#     })

# def userPanel(request):
#     user = request.user
#     appointments = Appointment.objects.filter(user=user).order_by('day', 'time')
#     return render(request, 'userPanel.html', {
#         'user':user,
#         'appointments':appointments,
#     })

# def userUpdate(request, id):
#     appointment = Appointment.objects.get(pk=id)
#     userdatepicked = appointment.day
#     #Copy  booking:
#     today = datetime.today()
#     minDate = today.strftime('%Y-%m-%d')

#     #24h if statement in template:
#     delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
#     #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
#     weekdays = validWeekday(22)

#     #Only show the days that are not full:
#     validateWeekdays = isWeekdayValid(weekdays)
    

#     if request.method == 'POST':
#         service = request.POST.get('service')
#         day = request.POST.get('day')

#         #Store day and service in django session:
#         request.session['day'] = day
#         request.session['service'] = service

#         return redirect('userUpdateSubmit', id=id)


#     return render(request, 'userUpdate.html', {
#             'weekdays':weekdays,
#             'validateWeekdays':validateWeekdays,
#             'delta24': delta24,
#             'id': id,
#         })

# def userUpdateSubmit(request, id):
#     user = request.user
#     times = [
#         "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
#     ]
#     today = datetime.now()
#     minDate = today.strftime('%Y-%m-%d')
#     deltatime = today + timedelta(days=21)
#     strdeltatime = deltatime.strftime('%Y-%m-%d')
#     maxDate = strdeltatime

#     day = request.session.get('day')
#     service = request.session.get('service')
    
#     #Only show the time of the day that has not been selected before and the time he is editing:
#     hour = checkEditTime(times, day, id)
#     appointment = Appointment.objects.get(pk=id)
#     userSelectedTime = appointment.time
#     if request.method == 'POST':
#         time = request.POST.get("time")
#         date = dayToWeekday(day)

#         if service != None:
#             if day <= maxDate and day >= minDate:
#                 if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
#                     if Appointment.objects.filter(day=day).count() < 11:
#                         if Appointment.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
#                             AppointmentForm = Appointment.objects.filter(pk=id).update(
#                                 user = user,
#                                 service = service,
#                                 day = day,
#                                 time = time,
#                             ) 
#                             messages.success(request, "Appointment Edited!")
#                             return redirect('index')
#                         else:
#                             messages.success(request, "The Selected Time Has Been Reserved Before!")
#                     else:
#                         messages.success(request, "The Selected Day Is Full!")
#                 else:
#                     messages.success(request, "The Selected Date Is Incorrect")
#             else:
#                     messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
#         else:
#             messages.success(request, "Please Select A Service!")
#         return redirect('userPanel')


#     return render(request, 'userUpdateSubmit.html', {
#         'times':hour,
#         'id': id,
#     })

# def staffPanel(request):
#     today = datetime.today()
#     minDate = today.strftime('%Y-%m-%d')
#     deltatime = today + timedelta(days=21)
#     strdeltatime = deltatime.strftime('%Y-%m-%d')
#     maxDate = strdeltatime
#     #Only show the Appointments 21 days from today
#     items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

#     return render(request, 'staffPanel.html', {
#         'items':items,
#     })

# def dayToWeekday(x):
#     z = datetime.strptime(x, "%Y-%m-%d")
#     y = z.strftime('%A')
#     return y

# def validWeekday(days):
#     #Loop days you want in the next 21 days:
#     today = datetime.now()
#     weekdays = []
#     for i in range (0, days):
#         x = today + timedelta(days=i)
#         y = x.strftime('%A')
#         if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
#             weekdays.append(x.strftime('%Y-%m-%d'))
#     return weekdays
    
# def isWeekdayValid(x):
#     validateWeekdays = []
#     for j in x:
#         if Appointment.objects.filter(day=j).count() < 10:
#             validateWeekdays.append(j)
#     return validateWeekdays

# def checkTime(times, day):
#     #Only show the time of the day that has not been selected before:
#     x = []
#     for k in times:
#         if Appointment.objects.filter(day=day, time=k).count() < 1:
#             x.append(k)
#     return x

# def checkEditTime(times, day, id):
#     #Only show the time of the day that has not been selected before:
#     x = []
#     appointment = Appointment.objects.get(pk=id)
#     time = appointment.time
#     for k in times:
#         if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
#             x.append(k)
#     return x





# # def connexion(request):
# #     if request.method =="POST":
# #         username = request.POST['username']
# #         password = request.POST['password']
# #         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "vous etes connecté")
#             #return redirect ('connectes')
        
#         else:
#             messages.error(request, "vous avez pas les bons identifiants")
#         # Return an 'invalid login' error message.
    
    
    # return render(request, 'testy/connexion.html')
    
    
    # def login(request):
#     return (request, 'rendez_vous/login.html')

# def logout(request):
#     return (request, 'rendez_vous/logout.html')