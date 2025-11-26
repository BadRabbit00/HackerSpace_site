from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import User
from .utils import verify_telegram_data

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if not next_url:
                next_url = 'home'
            return redirect(next_url)
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})

    return render(request, 'users/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'users/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'users/signup.html')

def telegram_login_callback(request):
    data = request.GET.dict()
    if verify_telegram_data(data):
        telegram_id = data.get('id')
        username = data.get('username')
        
        try:
            user = User.objects.get(telegram_id=telegram_id)
            login(request, user)
        except User.DoesNotExist:
            # Create new user linked to this telegram_id
            new_username = username if username else f"tg_{telegram_id}"
            counter = 1
            while User.objects.filter(username=new_username).exists():
                new_username = f"{username}_{counter}" if username else f"tg_{telegram_id}_{counter}"
                counter += 1
            
            user = User.objects.create_user(username=new_username, telegram_id=telegram_id)
            user.set_unusable_password()
            user.save()
            login(request, user)
            
        return redirect('home')
    return redirect('login')

@login_required
def link_telegram_callback(request):
    data = request.GET.dict()
    if verify_telegram_data(data):
        telegram_id = data.get('id')
        
        # Check if this telegram_id is already used by another user
        if User.objects.filter(telegram_id=telegram_id).exclude(id=request.user.id).exists():
             messages.error(request, "Этот Telegram аккаунт уже привязан к другому пользователю.")
             return redirect('connect_telegram')

        request.user.telegram_id = telegram_id
        request.user.save()
        return redirect('home')
    return redirect('connect_telegram')

@login_required
def connect_telegram_view(request):
    if not getattr(settings, 'TELEGRAM_AUTH_REQUIRED', True):
        return redirect('home')
        
    if request.user.telegram_id:
        return redirect('home')
    return render(request, 'users/connect_telegram.html')
