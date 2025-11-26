def can_user_borrow(user):
    """
    Единая точка истины.
    Возвращает (bool, reason).
    """
    # 1. Проверяем наличие профиля
    if not hasattr(user, 'profile'):
        return False, "Нет профиля"

    # 2. Проверяем доступ в спейс (Активен или Grace Period)
    if not user.profile.has_access_to_space:
        return False, "Нет активной подписки (или льготный период истек)"

    # 3. Проверяем документы
    if not hasattr(user, 'personal_data'):
        return False, "Не загружены документы"
    
    if user.personal_data.verification_status != 'approved':
        return False, "Документы не подтверждены менеджером"

    return True, "OK"
