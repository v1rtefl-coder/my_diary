import os
import django
from django.conf import settings

# Настройки для тестов
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Временно меняем БД на SQLite для тестов
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',  # База в памяти (быстрая)
}

django.setup()

from django.test.utils import get_runner
from django.core.management import call_command

# Запускаем тесты
call_command('test', 'entries.tests.DiaryEntryModelTest', verbosity=2)
