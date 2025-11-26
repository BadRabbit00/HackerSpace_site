# 🐇 BlackIce HackerSpace Portal

![Status](https://img.shields.io/badge/Status-In%20Development-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2-092E20)
![Redis](https://img.shields.io/badge/Redis-Cache-red)

Официальный портал первого хакерспейса в Средней Азии **"BlackIce"**. 
Система управления сообществом, контентом и ресурсами пространства с уникальным Cyberpunk-дизайном.

---

## ⚡ Основные возможности

### 👤 Пользователи и Резиденство
*   **Профили**: Расширенные профили пользователей с привязкой GitHub/Telegram.
*   **Подписки**: Система тарифных планов (`SubscriptionPlan`). Статус "Резидент" выдается автоматически при активной подписке.
*   **Контроль доступа**: Логика проверки доступа в помещение (`grants_resident_status`, Grace Period).

### 📰 Контент и События
*   **Новости**: Система публикации новостей. Автоматическая генерация превью-карточек (`NewsCard`) через Django Signals.
*   **События**: Календарь мероприятий с регистрацией.
*   **Интеграция**: Вывод последних новостей и событий на главную страницу с кэшированием.

### 🛠 Оборудование (Inventory)
*   **Каталог**: Список доступного "железа" (Hardware).
*   **Аренда**: Система выдачи предметов (`Loan`). Проверка доступности, статуса резидента и занятости предмета.

### 🎨 UI/UX (Cyberpunk Theme)
*   **Дизайн**: Темная тема, неоновые акценты, шрифт Orbitron.
*   **Эффекты**: JS-эффекты "Glitch" (глюки текста), кастомные карусели с нативным скроллом.
*   **Интерактивность**: Приветственные баннеры с запоминанием через Cookies.

### 🚀 Производительность
*   **Redis Caching**: 
    *   Кэширование счетчика резидентов (24 часа).
    *   Кэширование блоков главной страницы (Новости, Ивенты, Оборудование).
*   **Signals**: Автоматическая инвалидация кэша при обновлении контента.

---

## 🛠 Технологический стек

*   **Backend**: Python 3, Django 5.2.8
*   **Database**: SQLite (Dev) / PostgreSQL (Prod)
*   **Cache**: Redis (via `django-redis`)
*   **Frontend**: Django Templates, Vanilla JS, CSS3 (Grid/Flexbox)
*   **Containerization**: Docker, Docker Compose

---

## 🚀 Установка и запуск (Local)

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/BadRabbit00/HackerSpace_site.git
    cd HackerSpace_site
    ```

2.  **Создайте виртуальное окружение:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте переменные окружения:**
    Создайте файл `.env` в корне проекта (см. раздел Конфигурация).

5.  **Примените миграции:**
    ```bash
    python manage.py migrate
    ```

6.  **Запустите сервер:**
    ```bash
    python manage.py runserver
    ```

---

## 🐳 Запуск через Docker

Проект поддерживает гибкую конфигурацию через профили Docker Compose.

**1. Полный стек (PostgreSQL + Redis + Nginx)**
```bash
docker compose --profile full up --build
```

**2. Только SQLite + Redis (Рекомендуется для Dev)**
```bash
docker compose --profile redis up --build
```

**3. Минимальный запуск (только Django)**
```bash
docker compose up --build
```

---

## ⚙️ Конфигурация (.env)

Пример файла `.env`:

```env
DEBUG=1
SECRET_KEY=your_super_secret_key_here
ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# База данных (sqlite или postgres)
DATABASE=sqlite
# Если postgres:
SQL_DATABASE=hackerspace_db
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432

# Кэширование
USE_REDIS=True
REDIS_URL=redis://127.0.0.1:6379/1

# Telegram Bot (опционально)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_AUTH_REQUIRED=True
```

---

## 📂 Структура проекта

*   `account/` - Управление подписками, профилями и платежами.
*   `events/` - Система мероприятий.
*   `inventory/` - Учет и аренда оборудования.
*   `news/` - Новости и блог.
*   `users/` - Кастомная модель пользователя и аутентификация.
*   `website/` - Главная страница, статика, глобальные контекст-процессоры.
*   `forum/` - Форум для общения.
