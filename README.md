#  Дневник успеха

Веб-приложение для ведения личного дневника по методике Доминика Спентса "6-минутный дневник".

##  Возможности

-  Регистрация и аутентификация пользователей
-  Утренний ритуал (3 минуты):
-  Благодарности
-  Аффирмации
-  Цели на день
-  Вечерний ритуал (3 минуты):
-  Победы дня
-  Уроки и улучшения
-  Отслеживание настроения
-  Поиск по записям
-  Статистика успеха
-  Современный адаптивный дизайн на Bootstrap
-  Работает на всех устройствах

##  Технологии

- Python 3.13
- Django 6.0.5
- PostgreSQL
- Bootstrap 5
- Docker & Docker Compose

##  Установка и запуск

### Локальный запуск (без Docker)

# Клонируйте репозиторий
```
git clone <your-repo-url>
cd my_diary
```

# Создайте виртуальное окружение
```
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

# Установите зависимости
```
pip install -r requirements.txt
```


# Настройте переменные окружения (.env файл)
```
cp .env.example .env
# Отредактируйте .env под вашу БД
```

# Выполните миграции
```
python manage.py migrate
```

# Создайте суперпользователя
```
python manage.py createsuperuser
```

# Запустите сервер
```
 manage.py runserver
```

# Запуск с Docker
```
docker-compose up --build
```

# Доступные страницы

- Главная: http://127.0.0.1:8000/

- Регистрация: http://127.0.0.1:8000/register/

- Вход: http://127.0.0.1:8000/login/

- Утренний ритуал: http://127.0.0.1:8000/entries/morning/

- Админ-панель: http://127.0.0.1:8000/admin/

# Тестовый пользователь

Логин: admin
Пароль: admin123

# Структура проекта

my_diary/
├── accounts/              # Приложение пользователей
├── config/                # Настройки проекта
├── entries/               # Приложение записей
├── media/                 # Загруженные файлы
├── static/                # Статические файлы
├── templates/             # HTML шаблоны
├── requirements.txt       # Зависимости
├── Dockerfile             # Конфигурация Docker
├── docker-compose.yml     # Docker Compose
└── README.md              # Документация