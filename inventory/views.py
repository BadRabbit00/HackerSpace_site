from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Item, Loan
from .utils import can_user_borrow

@login_required
def take_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # 1. Проверка: Доступна ли вещь вообще?
    if not item.is_available_for_loan:
        messages.error(request, "Этот предмет нельзя взять.")
        return redirect('hardware_list') # Или куда-то еще

    # 2. ГЛАВНАЯ ПРОВЕРКА (Твоя утилита)
    allowed, reason = can_user_borrow(request.user)
    if not allowed:
        messages.error(request, f"Ошибка доступа: {reason}")
        return redirect('account_dashboard')

    # 3. Проверка: Не занята ли вещь прямо сейчас?
    active_loan = Loan.objects.filter(item=item, status__in=['active', 'requested', 'overdue']).exists()
    if active_loan:
        messages.error(request, "Предмет сейчас у кого-то на руках.")
        return redirect('hardware_list')

    if request.method == 'POST':
        # 4. Создаем аренду
        loan = Loan(
            item=item,
            borrower=request.user,
            deadline=timezone.now() + timezone.timedelta(days=14), # Например, на 2 недели
            purpose=request.POST.get('purpose', 'Личное использование')
        )

        # 5. Логика статуса
        if item.owner is None:
            # Вещь Спейса -> Сразу выдаем (так как can_user_borrow уже прошел)
            loan.status = 'active'
            loan.taken_at = timezone.now()
            msg = "Предмет выдан! Не забудьте вернуть через 2 недели."
            
            # ТУТ БУДЕТ ГЕНЕРАЦИЯ PDF И ОТПРАВКА В TELEGRAM
            # send_loan_receipt_task.delay(loan.id) 
            
        else:
            # Вещь Резидента -> Ждем одобрения владельца
            loan.status = 'requested'
            msg = "Запрос отправлен владельцу предмета."
            # send_request_to_owner_task.delay(item.owner.id, loan.id)

        loan.save()
        messages.success(request, msg)
        return redirect('account_dashboard')

    # Если GET запрос - показываем страницу подтверждения
    return render(request, 'inventory/take_confirm.html', {'item': item})
