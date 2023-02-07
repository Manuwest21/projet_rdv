from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns =[
	# path('',views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', auth_views.LoginView.as_view(template_name='rendez_vous/home.html'), name = 'login'),
    path('login/', auth_views.LoginView.as_view(template_name='connexion/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='connexion/logout.html'), name = 'logout'),
]