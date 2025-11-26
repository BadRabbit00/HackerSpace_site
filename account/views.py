from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory import models
from inventory.models import Loan

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')

def my_loans(request):
    # Дай мне все записи, где Я заемщик и статус АКТИВЕН или ПРОСРОЧЕН
    active_loans = Loan.objects.filter(
        borrower=request.user, 
        status__in=['active', 'overdue']
    )
    return render(request, 'inventory/my_loans.html', {'loans': active_loans})
