from django.urls import path
from . import views
from .feeds import LatestCardsFeed
from django.contrib.auth import views as auth_views

#using the app named mtg
app_name = 'mtg'

# setting URL patterns equal to appropriate paths.
urlpatterns = [
    #Example would be website.com/card_list, Pattern for card list
    path('', views.card_list, name='card_list'),
    # Patter for card view based on tags
    path(
        'tag/<slug:tag_slug>/', views.card_list, name='card_list_by_tag'
    ),
    #Example would be website.com/1/lanowar-elves/card_detail, pattern for card details
    path('<int:id>/<slug:card>', views.card_detail, name='card_detail'),
    #Pattern for form access
    path('<int:card_id>/share/', views.card_share, name='card_share'),
    # Pattern for card comment access
    path('<int:card_id>/comment/', views.card_comment, name='card_comment'),
    path('feed/', LatestCardsFeed(), name='card_feed'),
    path('search/', views.card_search, name='card_search'),
    path('create/', views.deck_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.deck_detail, name='deck_detail'),
    path('like/', views.deck_like, name='like'),
]