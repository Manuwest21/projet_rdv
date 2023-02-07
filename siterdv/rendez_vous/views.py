from django.shortcuts import render, redirect
from django.http import HttpResponse
# from testy.forms import ContactUsForm, EtudiantForm
# from testy.register import UserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rendez_vous.forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rendez_vous.models import Note
# Create your views here.


# def home (request):
#     return render (request, 'rendez_vous/home.html')
@login_required
def home(request):
	context ={
	'notes': Note.objects.all()
	}
	return render(request, 'rendez_vous/home.html',context)

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


# def connexion(request):
#     if request.method =="POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
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