# 🐇 BlackIce HackerSpace Portal

![Status](https://img.shields.io/badge/Status-Active%20Development-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.x-092E20)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Async%20Tasks-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

Официальный портал хакерспейса **"BlackIce"**. 
Комплексная система управления сообществом, инвентарем, событиями и документами с уникальным Cyberpunk-дизайном.

Проект построен на микросервисной архитектуре: Django отвечает за веб-интерфейс и бизнес-логику, а тяжелые задачи (генерация документов) вынесены в фоновые воркеры через RabbitMQ.

---

## ⚡ Основные возможности

### 👤 Пользователи и Роли (RBAC)
*   **Профили**: Расширенные профили с аватарами, био и соцсетями.
*   **Подписки**: Система тарифных планов. Автоматическое присвоение статуса "Резидент".
*   **Группы доступа**: Разделение прав через Django Groups:
    *   `Event Managers`: Создание и модерация ивентов.
    *   `News Editors`: Публикация новостей.
    *   `Inventory Managers`: Управление оборудованием спейса.

### 🛠 Инвентарь и Шеринг (Inventory)
*   **Гибридное владение**: Предметы могут принадлежать Спейсу или конкретному Резиденту.
*   **Аренда (Loans)**: 
    *   Проверка доступности и прав доступа (Grace Period).
    *   Защита от "само-аренды".
    *   Статусы: `Requested` (для личных вещей), `Active` (авто-выдача вещей спейса).
*   **Управление**: Владельцы могут скрывать свои предметы из поиска или забирать их (удалять из системы) через дашборд.

### 📅 События (Events)
*   **Менеджмент**: Создание и редактирование ивентов через удобные модальные окна.
*   **Участие**: Кнопка "Join" с проверкой требований подписки.
*   **Хостинг**: Возможность назначить организатора (Host) при создании события.

### 📄 Документооборот (Async PDF)
*   **Генерация контрактов**: При взятии предмета в аренду автоматически генерируется PDF-акт приема-передачи.
*   **Архитектура**: 
    *   Django отправляет задачу в очередь `RabbitMQ`.
    *   Отдельный контейнер `worker` (Pika + ReportLab) забирает задачу.
    *   Генерируется PDF с поддержкой кириллицы (DejaVu Fonts) и прикрепляется к объекту аренды.

### 🎨 UI/UX
*   **Cyberpunk Style**: Темная тема, неоновые границы, Glassmorphism.
*   **Dashboard**: Единый центр управления для пользователя (профиль, ивенты, аренды, мои предметы).
*   **Интерактивность**: Flatpickr для дат, модальные окна для редактирования без перезагрузки страниц.

---

## 🛠 Технологический стек

*   **Backend**: Django 5.x
*   **Database**: SQLite (Dev) / PostgreSQL (Prod)
*   **Message Broker**: RabbitMQ
*   **Worker**: Python script (`document_creater/consumer.py`) + ReportLab
*   **Frontend**: Django Templates, CSS3 Variables, Vanilla JS
*   **Containerization**: Docker, Docker Compose

---

## 🐳 Запуск через Docker (Рекомендуется)

Проект полностью докеризирован. Включает сервисы: `web` (Django), `db` (Postgres), `rabbitmq`, `worker`, `nginx`.

### 1. Запуск полного стека
```bash
docker compose --profile full up --build
```
*Это поднимет Django, Postgres, RabbitMQ, Worker и Nginx.*

### 2. Суперпользователь (автоматическое создание)

При запуске через Docker, суперпользователь с именем **BadRabbit** создается автоматически (см. `entrypoint.sh`). 

Для задания пароля и email используйте переменные окружения:
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL`

Если автоматическое создание не сработало или требуется другой суперпользователь, выполните вручную:
```bash
docker compose exec web python manage.py createsuperuser
```

### 3. Инициализация ролей
Для создания стандартных групп (Event Managers, News Editors, etc.) выполните команду:
```bash
docker compose exec web python manage.py setup_roles
```

---

## 🚀 Локальная разработка (без Docker)

Если вы хотите запустить проект локально (вам понадобится запущенный RabbitMQ отдельно или отключение функционала PDF):

1.  **Установка зависимостей:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Миграции:**
    ```bash
    python manage.py migrate
    ```

3.  **Настройка ролей:**
    ```bash
    python manage.py setup_roles
    ```

4.  **Запуск:**
    ```bash
    python manage.py runserver
    ```

*Примечание: Для работы генерации документов локально, вам нужно запустить RabbitMQ и скрипт воркера вручную:*
```bash
python document_creater/consumer.py
```

---

## 📂 Структура проекта

*   `HackerSpace/` - Основные настройки проекта.
*   `account/` - Личный кабинет, дашборд, профили.
*   `events/` - Приложение событий.
*   `inventory/` - Логика предметов и аренды.
*   `document_creater/` - Логика микросервиса генерации PDF (Consumer).
*   `users/` - Кастомная модель пользователя и команды управления (`setup_roles`).
*   `news/` - Новостной движок.
*   `website/` - Лендинг и статика.

---

## 🛡 Права доступа (Permissions)

Система использует стандартные права Django.
*   **Event Managers**: `events.add_event`, `events.change_event`
*   **News Editors**: `news.add_news`, `news.change_news`
*   **Inventory Managers**: `inventory.add_item`, `inventory.change_item`

Назначить пользователя в группу можно через админку: `/admin/`.

---

## ⚙️ Переменные окружения (.env)

```env
DEBUG=1
SECRET_KEY=your_secret
ALLOWED_HOSTS=localhost 127.0.0.1

# Database
DATABASE=postgres # или sqlite
SQL_DATABASE=hackerspace_db
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432

# RabbitMQ
RABBITMQ_HOST=rabbitmq
```
