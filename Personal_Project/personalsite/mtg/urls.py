from django.urls import path
from . import views

#using the app named mtg
app_name = 'mtg'

# setting URL patterns equal to appropriate paths.
urlpatterns = [
    #Example would be website.com/card_list
    path('', views.card_list, name='card_list'),
    #Example would be website.com/1/card_detail
    path('<int:id>/', views.card_detail, name='card_detail'),
]