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
    
    #url login to access the html page from the view
    #path('login/', views.user_login, name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard,name='dashboard'),
        # change password urls
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
        # reset password urls
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]