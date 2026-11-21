from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import *


class OrderForm(ModelForm):
    class Meta:
        model = order
        fields = ('name', 'phone', 'game')
        labels = {
            'name': 'Ваше имя',
            'phone': 'Номер телефона',
            'game': 'Игра',
        }
def tickets(request):
    all_games = games.objects.all().order_by('date')
    return render(request, 'sport/tickets.html', {'games': all_games})


def buy_ticket(request, game_id=None):
    if not request.user.is_authenticated:
        return redirect('login')
    selected_game = get_object_or_404(games, pk=game_id) if game_id else None
    form = OrderForm(request.POST if request.method == 'POST' else None,initial={'game': selected_game},)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        messages.success(request, 'Билет успешно заказан!')
        return redirect('tickets')
    return render(request, 'sport/buy_ticket.html', {
        'form': form, 'selected_game': selected_game,
    })


def home(request):
    upcoming_games = games.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    return render(request, 'sport/home.html', {'games': upcoming_games})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'sport/login.html', {'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'sport/register.html', {'form': form})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = order.objects.filter(user=request.user)
    return render(request, 'sport/profile.html', {'orders': orders})
