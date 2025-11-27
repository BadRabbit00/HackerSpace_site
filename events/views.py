from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import EventForm

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            messages.success(request, 'Ивент успешно создан!')
            return redirect('account_dashboard')
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})
