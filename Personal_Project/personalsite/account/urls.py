from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
urlpatterns = [
    
    #url login to access the html page from the view
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]