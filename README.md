# 🏗️ CeramicGO - Система управления складом керамической плитки

CeramicGO - это Telegram-бот и веб-приложение на Django для управления складом и продажей керамической плитки.

## 🚀 Стек технологий
- 🐍 **Backend**: Django, Django REST Framework
- 🤖 **Bot**: pyTelegramBotAPI
- 🗄️ **Database**: PostgreSQL
- ⚡ **Cache & State Management**: Redis
- 🐳 **Containerization**: Docker, Docker Compose
- 🎭 **Package Management**: Poetry

## 📌 Описание проекта
**CeramicGO** позволяет удобно управлять складом керамической плитки через Telegram-бота и веб-интерфейс Django.
### 🔹 Функции Telegram-бота:
- 📥 Добавление, редактирование, удаление товаров (CRUD)
- 📊 Учет складских остатков
- 🔍 Получение информации о товаре
- 🔑 Авторизация пользователей

### 🔹 Функции Django-админки:
- 📦 Управление товарами и складом
- 👥 Управление пользователями Telegram-бота
- 🛠️ Фильтрация и поиск записей

---

## 🛠️ Установка и запуск

### 1️⃣ Клонирование репозитория
```sh
git clone https://github.com/mrustam9929/CeramicGo.git
cd CeramicGO
```

### 2️⃣ Настройка `.env`
Создайте `.env` файл в корне проекта и добавьте переменные окружения:

```ini
# 🔧 Режим работы приложения
DEVELOPMENT_MODE=PRODUCTION  # или DEVELOPMENT для разработки

# 🔐 Настройки Django
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://localhost

# 🗄️ Настройки базы данных PostgreSQL
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=MySuperSecretPassword
POSTGRES_HOST=db
POSTGRES_PORT=5432

# 🤖 Настройки Telegram-бота
TG_BOT_TOKEN=your_telegram_bot_token
TG_WEBHOOK_URL=https://yourdomain.com/tg-webhook/

# ⚡ Настройки Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

### 3️⃣ Установка зависимостей с Poetry
```sh
poetry install
```

### 4️⃣ Запуск в Docker
```sh
docker-compose up -d --build
```

### 5️⃣ Создание суперпользователя Django
```sh
docker-compose exec backend python manage.py createsuperuser
```

### 6️⃣ Установка вебхука для бота
```sh
docker-compose exec backend python manage.py set_webhook
```

### 7️⃣ Запуск бота в режиме разработки
```sh
docker-compose exec backend python manage.py start_bot
```

---

## ⚙️ Основные команды
| Команда                                                        | Описание                       |
|----------------------------------------------------------------|--------------------------------|
| `poetry install`                                               | Установить зависимости         |
| `docker-compose up -d --build`                                 | Запустить проект в контейнерах |
| `docker-compose exec backend python manage.py createsuperuser` | Создать администратора Django  |
| `docker-compose exec backend python manage.py set_webhook`     | Установить вебхук для бота     |
| `docker-compose exec backend python manage.py start_bot`       | Запустить бота вручную         |

---

## 📂 Монтируемые папки
В `docker-compose.yml` используются монтируемые папки:
- `mounts/src/logs/` — логи работы backend-а
- `mounts/src/static/` — статические файлы Django
- `mounts/src/media/` — загруженные пользователями файлы
- `mounts/db/pg_data/` — данные PostgreSQL
- `mounts/db/backups/` — резервные копии базы данных
- `mounts/db/logs/` — логи работы PostgreSQL
- `mounts/redis/data/` — данные Redis
- `mounts/redis/conf/` — конфигурационные файлы Redis

---

## 🔗 Доступы
- **Django Admin Panel**: [`http://localhost:8000/admin/`](http://localhost:8000/admin/)
---

## 📜 Лицензия
Этот проект распространяется по лицензии MIT. Подробнее см. в файле [`LICENSE`](LICENSE).

© 2024 Рустам Мухтаров

