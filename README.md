# BlackIce HackerSpace

Сайт для первого хакерспейса в Средней Азии "BlackIce".

## О проекте

Проект написан на Django. Представляет собой лендинг с информацией о хакерспейсе, оборудовании и новостях.

## Установка и запуск

1.  Клонируйте репозиторий.
2.  Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
3.  Активируйте виртуальное окружение:
    *   Windows: `venv\Scripts\activate`
    *   Linux/Mac: `source venv/bin/activate`
4.  Установите зависимости:
    ```bash
    pip install django
    ```
5.  Выполните миграции:
    ```bash
    python manage.py migrate
    ```
6.  Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

## Docker Запуск

Проект поддерживает гибкую конфигурацию через Docker Compose. Вы можете выбирать базу данных (SQLite/PostgreSQL) и кэш (LocalMem/Redis).

### Предварительная настройка

1.  Создайте файл `.env` (можно скопировать из `.env.example` если есть, или использовать созданный автоматически):
    ```env
    DEBUG=1
    SECRET_KEY=your_secret_key
    ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    
    # Настройки БД
    # DATABASE=postgres или sqlite
    DATABASE=postgres
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=hello_django_dev
    SQL_USER=hello_django
    SQL_PASSWORD=hello_django
    SQL_HOST=db
    SQL_PORT=5432

    # Настройки Redis
    # USE_REDIS=True или False
    USE_REDIS=True
    ```

### Варианты запуска

**1. Полный стек (PostgreSQL + Redis + Nginx)**
```bash
docker compose --profile full up --build
```
*В `.env` должно быть: `DATABASE=postgres`, `USE_REDIS=True`*

**2. PostgreSQL без Redis**
```bash
docker compose --profile postgres up --build
```
*В `.env` должно быть: `DATABASE=postgres`, `USE_REDIS=False`*

**3. SQLite + Redis**
```bash
docker compose --profile redis up --build
```
*В `.env` должно быть: `DATABASE=sqlite`, `USE_REDIS=True`*

**4. Только SQLite (Минимальный набор)**
```bash
docker compose up --build
```
*В `.env` должно быть: `DATABASE=sqlite`, `USE_REDIS=False`*

### Полезные команды

*   Создать суперпользователя:
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```
*   Остановить контейнеры:
    ```bash
    docker compose down
    ```

## Функционал

*   Главная страница с информацией о хакерспейсе.
*   Карусель с доступным оборудованием.
*   Блок новостей.
*   Счетчик резидентов.
