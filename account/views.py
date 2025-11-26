from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from inventory.models import Loan, Item
from events.models import Event
from .models import SubscriptionPlan, Payment

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
    next_month = today + timedelta(days=30)
    
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

@login_required
def pricing_view(request):
    plans = SubscriptionPlan.objects.filter(is_public=True)
    profile = getattr(request.user, 'profile', None)
    current_plan = profile.current_plan if profile else None
    
    # If user has a paid plan (price > 0), hide free plans (price = 0)
    if current_plan and current_plan.price > 0:
        plans = plans.exclude(price=0)
        
    return render(request, 'account/pricing.html', {
        'plans': plans,
        'current_plan': current_plan
    })

@login_required
def initiate_payment(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    claim_student = request.GET.get('student', 'false') == 'true'
    
    price_to_pay = plan.price

    if claim_student:
        if not plan.student_price:
             messages.error(request, "У этого тарифа нет студенческой скидки.")
             return redirect('pricing')

        # Check if user has personal_data
        if not hasattr(request.user, 'personal_data'):
             messages.warning(request, "Чтобы получить скидку, заполните профиль и загрузите фото студенческого!")
             return redirect('upload_documents') 

        if not request.user.personal_data.student_document:
            messages.warning(request, "Чтобы получить скидку, загрузите фото студенческого!")
            return redirect('upload_documents')
            
        if request.user.personal_data.verification_status != 'approved':
            messages.warning(request, "Ваши документы еще на проверке. Дождитесь подтверждения или оплатите полную стоимость.")
            return redirect('account_dashboard')

        price_to_pay = plan.student_price

    # Create payment
    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=price_to_pay, 
        status='completed'
    )
    
    # Update Profile
    profile = request.user.profile
    profile.current_plan = plan
    profile.subscription_end_date = timezone.now().date() + timedelta(days=plan.duration_days)
    profile.save()
    
    return render(request, 'account/payment_success.html', {'plan': plan})

def my_loans(request):
    # Дай мне все записи, где Я заемщик и статус АКТИВЕН или ПРОСРОЧЕН
    active_loans = Loan.objects.filter(
        borrower=request.user, 
        status__in=['active', 'overdue']
    )
    return render(request, 'inventory/my_loans.html', {'loans': active_loans})
