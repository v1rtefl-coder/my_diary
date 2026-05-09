from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('entries:list')  # Исправлено

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('entries:list')  # Исправлено
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# Добавляем представление для главной страницы
def home(request):
    if request.user.is_authenticated:
        return redirect('entries:list')
    return redirect('accounts:login')
