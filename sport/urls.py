from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('tickets/', tickets, name='tickets'),
    path('tickets/buy/', buy_ticket, name='buy_ticket'),
    path('tickets/buy/<int:game_id>/', buy_ticket, name='buy_ticket_for_game'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
]