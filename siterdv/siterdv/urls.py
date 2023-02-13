"""siterdv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rendez_vous import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_authen.url')),
    path('',views.home, name='home'),
    path('home/',views.home, name='home'),
    path('register/', views.register, name="register"),
    path('login/',views.login_p, name="login_p"),
    path('loggout/', views.loggout, name="loggout"),
    path('profil_perso/', views.profil_perso, name="profil_perso"),
    path('add_note/<nom_user_rdv>/',views.add_note,name='add_note'),
    path('reserver/',views.rdv,name='reserver'),
    path('mes_rdv', views.mes_rdv, name='mes_rdv'),
    path('list_all_rdv/', views.list_all_rdv, name='list_all_rdv'),
    path('note_user', views.note_user, name='note_user'),
    path('confirmation_rdv', views.confirmation_rdv, name='confirmation_rdv'),
    path('notes_ciblees', views.notes_ciblees,name='notes_ciblees')
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('booking', views.booking, name='booking'),
    # path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    # path('user-panel', views.userPanel, name='userPanel'),
    # path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    # path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
    # path('staff-panel', views.staffPanel, name='staffPanel'),
]
