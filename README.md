# DjangoSite (projectDjango)
# ProjectDjango (Umbrella Lab)

Небольшое Django-приложение для работы с:
- исследователями (`Researcher`)
- патогенами (`Pathogen`)

Интерфейс: кастомный CSS в стиле Umbrella (`static/css/umbrella.css`), CRUD-страницы и авторизация.

## Стек

- Python 3.13+
- Django 6
- SQLite
- Pillow (изображения)
- Gunicorn + Nginx (для Docker-режима)

## Быстрый запуск локально (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

После запуска:
- приложение: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- админка: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Основные переменные:
- `DJANGO_SECRET_KEY` - секретный ключ Django
- `DJANGO_DEBUG` - `1`/`0` для debug-режима
- `DJANGO_ALLOWED_HOSTS` - список хостов через запятую
- `DJANGO_CSRF_TRUSTED_ORIGINS` - trusted origins для CSRF
- `DJANGO_DB_PATH` - путь к sqlite базе (по умолчанию `db.sqlite3`)

## Запуск через Docker

```bash
docker compose up --build
```

Сервисы:
- `web` (Django + gunicorn, порт внутри контейнера `8080`)
- `nginx` (публикует `80:80`)

Приложение будет доступно на [http://localhost/](http://localhost/).

## Основные маршруты

- `/` - главная
- `/pathogens/` - список патогенов
- `/researchers/` - список исследователей
- `/accounts/login/` - вход
- `/accounts/register/` - регистрация
- `/admin/` - Django admin

## Структура проекта

- `projectDjango/` - настройки и корневые URL
- `resident/` - приложение (models/views/forms/urls/templates)
- `static/` - стили и статические ресурсы
- `media/` - загружаемые изображения
- `nginx/` - конфиг Nginx для Docker

---

## Локальная разработка (`runserver`)

1. Создайте виртуальное окружение и установите зависимости:

```powershell
cd d:\site\DjangoSite
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Примените миграции:

```powershell
python manage.py migrate
```

3. Запустите сервер разработки:

```powershell
python manage.py runserver
```

По умолчанию сайт будет на `http://127.0.0.1:8000/`.

### Переменные окружения (локально, по желанию)

Через `.env` или экспорт в PowerShell можно задать, например:

| Переменная | Назначение |
|------------|------------|
| `DJANGO_SECRET_KEY` | Секретный ключ (в проде обязателен свой) |
| `DJANGO_DEBUG` | `1` / `true` для отладки |
| `DJANGO_ALLOWED_HOSTS` | Список хостов через запятую (нужен для ngrok-домена) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Доверенные origin для CSRF (для HTTPS ngrok — `https://...`) |
| `DJANGO_DB_PATH` | Путь к SQLite (по умолчанию — `db.sqlite3` в корне проекта) |
| `DJANGO_USE_WHITENOISE` | `1` если нужен WhiteNoise для статики без отдельного веб-сервера |

Без `DJANGO_ALLOWED_HOSTS` / `DJANGO_CSRF_TRUSTED_ORIGINS` в коде уже есть значения по умолчанию для локальной работы, но для **нового домена ngrok** их нужно расширить 

---

## Запуск в Docker

Из корня репозитория (где лежат `Dockerfile` и `docker-compose.yml`):

```powershell
docker compose up --build
```

- **Nginx** слушает порт **80** на хосте и отдаёт статику/медиа, приложение — за прокси.
- Контейнер `web` поднимает Gunicorn на `8080` внутри сети compose (снаружи напрямую не проброшен).

Остановка: `Ctrl+C` или `docker compose down`.

### Файл `.env` (необязательно)

`docker-compose.yml` подхватывает `.env`, если он есть (`required: false`). Там удобно задать `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` и при необходимости переопределить хосты для своего окружения.

---

## ngrok «только с VPN»

Имеется в виду ситуация, когда **без VPN** ngrok не устанавливает туннель (блокировки, провайдер, корпоративная сеть, региональные ограничения), а **с включённым VPN** — работает. Тогда порядок такой:

1. **Включите VPN** и дождитесь стабильного соединения.
2. Запустите приложение так же, как обычно (`runserver` или Docker).
3. Посмотрите в консоль Django (или в адресную строку браузера), **какой URL и порт** у сервера. Обычно в логе что-то вроде: `Starting development server at http://127.0.0.1:8000/` — число **после двоеточия** (`8000` в этом примере) и есть порт, который нужно передать в ngrok. Если запускали, например, `runserver 0.0.0.0:9000`, берите **9000**.
4. В отдельном терминале:

   ```powershell
   ngrok http <ПОРТ_ИЗ_URL>
   ```

   Примеры: для `http://127.0.0.1:8000/` → `ngrok http 8000`; если сайт открывается как `http://localhost:80/` (часто для Docker с nginx) → `ngrok http 80`. Важно не угадывать «всегда 80», а ввести **тот порт, на котором у вас реально отвечает приложение в браузере**.

5. Скопируйте выданный публичный URL.

6. Укажите Django хост и origin для CSRF (иначе возможны `DisallowedHost` / ошибки CSRF):

   **PowerShell на сессию:**

   ```powershell
   $host = "xxxx.ngrok-free.app"
   $env:DJANGO_ALLOWED_HOSTS = "$host,.ngrok-free.app,.ngrok.io,localhost,127.0.0.1"
   $env:DJANGO_CSRF_TRUSTED_ORIGINS = "https://$host"
   python manage.py runserver
   ```

   Для Docker переопределите переменные в `.env` или в `docker-compose.yml` в секции `environment` у сервиса `web` (и при необходимости пересоберите/перезапустите compose), добавив ваш ngrok-домен в `DJANGO_ALLOWED_HOSTS` и `https://...` в `DJANGO_CSRF_TRUSTED_ORIGINS`.

---

## Полезные команды

| Задача | Команда |
|--------|---------|
| Миграции | `python manage.py migrate` |
| Создать суперпользователя | `python manage.py createsuperuser` |
| Статика в образе (Docker) | выполняется при старте `web` в compose |


