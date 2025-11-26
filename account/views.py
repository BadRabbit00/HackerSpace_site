from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from inventory.models import Loan, Item
from events.models import Event

@login_required
def dashboard(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    
    # 1. Inventory Data
    # Items owned by user stored in space (assuming location logic or just all owned items)
    my_items = Item.objects.filter(owner=user)
    
    # Items borrowed by user
    active_loans = Loan.objects.filter(borrower=user, status__in=['active', 'overdue'])
    pending_loans = Loan.objects.filter(borrower=user, status='requested')
    history_loans = Loan.objects.filter(borrower=user, status__in=['returned', 'late_returned'])

    # 2. Events Data
    today = timezone.now()
    next_month = today + timezone.timedelta(days=30)
    
    # Upcoming events (excluding ones user is already subscribed to)
    upcoming_events = Event.objects.filter(
        date__gte=today, 
        date__lte=next_month
    ).exclude(participants=user).order_by('date')
    
    # Events user is subscribed to
    subscribed_events = user.attended_events.filter(date__gte=today).order_by('date')
    
    # Events organized by user
    organized_events = user.hosted_events.filter(date__gte=today).order_by('date')

    context = {
        'profile': profile,
        'my_items': my_items,
        'active_loans': active_loans,
        'pending_loans': pending_loans,
        'history_loans': history_loans,
        'upcoming_events': upcoming_events,
        'subscribed_events': subscribed_events,
        'organized_events': organized_events,
    }
    
    return render(request, 'account/dashboard.html', context)

def my_loans(request):
    # Дай мне все записи, где Я заемщик и статус АКТИВЕН или ПРОСРОЧЕН
    active_loans = Loan.objects.filter(
        borrower=request.user, 
        status__in=['active', 'overdue']
    )
    return render(request, 'inventory/my_loans.html', {'loans': active_loans})
