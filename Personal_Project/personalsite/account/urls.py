from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    
    #url login to access the html page from the view
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/registration/logout.html'), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(template_name='account/registration/password_change_form.html'),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='account/registration/password_change_done.html'),
        name='password_change_done'
    ),
]