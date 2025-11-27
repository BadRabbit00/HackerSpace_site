from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Event
from .forms import EventForm

def event_list(request):
    today = timezone.now()
    two_months_later = today + timedelta(days=60)
    
    events = Event.objects.filter(
        date__gte=today,
        date__lte=two_months_later
    ).order_by('date')
    
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if already joined
    if request.user in event.participants.all():
        messages.info(request, "Вы уже записаны на этот ивент.")
        return redirect('event_list')

    # Check plan requirements
    if event.required_plan:
        user_plan = getattr(request.user.profile, 'current_plan', None)
        if not user_plan:
             messages.error(request, f"Для этого ивента требуется подписка: {event.required_plan.title}")
             return redirect('pricing')
        
        # Simple check: is user plan price >= required plan price? 
        # Or just check if they have ANY active plan if required_plan is set?
        # For now, let's assume if they have a plan, it's okay, or implement strict hierarchy later.
        # Let's just check if they have a plan for now.
        pass 

    event.participants.add(request.user)
    messages.success(request, f"Вы успешно записались на {event.title}!")
    return redirect('event_list')

@login_required
@permission_required('events.add_event', raise_exception=True)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            
            # Если в форме выбран хост - используем его, иначе - текущего юзера
            if not event.host:
                event.host = request.user
                
            event.save()
            messages.success(request, 'Ивент успешно создан!')
            return redirect('account_dashboard')
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check permission: Must be host OR have 'events.change_event' permission
    if event.host != request.user and not request.user.has_perm('events.change_event'):
        messages.error(request, "У вас нет прав на редактирование этого ивента.")
        return redirect('account_dashboard')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Ивент успешно обновлен!")
            return redirect('account_dashboard')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/create_event.html', {'form': form, 'is_edit': True})
