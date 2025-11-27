from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import datetime
import pika
import json
from .models import Item, Loan
from .utils import can_user_borrow

def hardware_list(request):
    # Получаем все доступные для аренды предметы
    items = Item.objects.filter(is_available_for_loan=True)

    # Исключаем предметы текущего пользователя, если он авторизован
    if request.user.is_authenticated:
        items = items.exclude(owner=request.user)

    # Сортируем по категории для группировки
    items = items.order_by('category', 'name')
    
    # Получаем ID предметов, которые сейчас заняты или запрошены
    unavailable_item_ids = Loan.objects.filter(
        status__in=['active', 'requested', 'overdue']
    ).values_list('item_id', flat=True)

    # Поиск
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(inventory_number__icontains=query)
        )

    context = {
        'items': items,
        'unavailable_item_ids': set(unavailable_item_ids), # set для быстрого поиска в шаблоне
    }
    return render(request, 'inventory/hardware_list.html', context)

@login_required
def my_loans(request):
    # Дай мне все записи, где Я заемщик и статус АКТИВЕН или ПРОСРОЧЕН
    active_loans = Loan.objects.filter(
        borrower=request.user, 
        status__in=['active', 'overdue']
    )
    return render(request, 'inventory/my_loans.html', {'loans': active_loans})

@login_required
def take_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # 1. Проверка: Доступна ли вещь вообще?
    if not item.is_available_for_loan:
        messages.error(request, "Этот предмет нельзя взять.")
        return redirect('hardware_list') # Или куда-то еще

    # 1.1 Проверка: Не пытается ли пользователь взять свою вещь?
    if item.owner == request.user:
        messages.error(request, "Вы не можете взять в аренду свой собственный предмет.")
        return redirect('hardware_list')

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
        return_date_str = request.POST.get('return_date')
        purpose = request.POST.get('purpose', 'Личное использование')

        if not return_date_str:
            messages.error(request, "Пожалуйста, укажите дату возврата.")
            return redirect('take_item', item_id=item.id)

        try:
            # Парсим дату из input type="date" (YYYY-MM-DD)
            return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()
            # Устанавливаем дедлайн на конец выбранного дня (23:59:59)
            deadline = timezone.make_aware(datetime.datetime.combine(return_date, datetime.time.max))
        except ValueError:
            messages.error(request, "Неверный формат даты.")
            return redirect('take_item', item_id=item.id)

        if deadline < timezone.now():
            messages.error(request, "Дата возврата не может быть в прошлом.")
            return redirect('take_item', item_id=item.id)

        # 4. Создаем аренду
        loan = Loan(
            item=item,
            borrower=request.user,
            deadline=deadline,
            purpose=purpose
        )

        # 5. Логика статуса
        if item.owner is None:
            # Вещь Спейса -> Сразу выдаем (так как can_user_borrow уже прошел)
            loan.status = 'active'
            loan.taken_at = timezone.now()
            msg = "Предмет выдан! Не забудьте вернуть через 2 недели."
            
            loan.save() # Сохраняем, чтобы получить ID

            # Отправка задачи на генерацию документа
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
                channel = connection.channel()
                channel.queue_declare(queue='document_generation')
                
                message = json.dumps({'loan_id': loan.id})
                channel.basic_publish(exchange='', routing_key='document_generation', body=message)
                connection.close()
            except Exception as e:
                print(f"RabbitMQ Error: {e}")
            
        else:
            # Вещь Резидента -> Ждем одобрения владельца
            loan.status = 'requested'
            msg = "Запрос отправлен владельцу предмета."
            loan.save()

        messages.success(request, msg)
        return redirect('account_dashboard')

    # Если GET запрос - показываем страницу подтверждения
    # Предлагаем дату возврата через 2 недели по умолчанию
    default_return_date = (timezone.now() + timezone.timedelta(days=14)).strftime('%Y-%m-%d')
    return render(request, 'inventory/take_confirm.html', {
        'item': item,
        'default_return_date': default_return_date
    })
