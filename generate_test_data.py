import os
import django
from datetime import datetime, timedelta
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from entries.models import DiaryEntry

User = get_user_model()

# Данные для генерации
GRATITUDES = [
    "Благодарен за здоровье и энергию",
    "Благодарен за поддержку близких",
    "Благодарен за возможность учиться новому",
    "Благодарен за вкусную еду и уютный дом",
    "Благодарен за новый опыт и возможности",
    "Благодарен за хорошую погоду и солнце",
    "Благодарен за верных друзей",
    "Благодарен за интересную работу",
    "Благодарен за своё тело и здоровье",
    "Благодарен за каждый прожитый день"
]

AFFIRMATIONS = [
    "Я уверен в себе и своих силах",
    "Каждый день я становлюсь лучше",
    "Я достоин успеха и счастья",
    "Я принимаю себя и люблю",
    "Я способен достичь любых целей",
    "Я открыт новым возможностям",
    "Я создаю свою идеальную жизнь",
    "Я благодарен за всё, что имею"
]

MORNING_GOALS = [
    "Завершить важный проект на работе",
    "Провести время с семьей",
    "Позаниматься спортом",
    "Прочитать книгу 30 минут",
    "Написать планы на неделю",
    "Освоить новую технологию",
    "Помочь коллеге с задачей",
    "Уделить время саморазвитию"
]

EVENING_WINS = [
    "Сегодня я выполнил все поставленные задачи",
    "Я помог коллеге решить сложную проблему",
    "Нашёл время для спорта и здоровья",
    "Провел качественное время с семьей",
    "Освоил новый навык или инструмент",
    "Сделал важный шаг к своей цели",
    "Прочитал полезную книгу",
    "Улучшил свои навыки общения"
]

IMPROVEMENTS = [
    "Можно было меньше отвлекаться на соцсети",
    "Стоило лучше планировать дневное время",
    "Нужно больше времени уделять отдыху",
    "Можно было ответить быстрее на письма",
    "Стоило выпить больше воды",
    "Нужно ложиться спать пораньше",
    "Можно было сделать больше за день",
    "Попробовать начать день раньше"
]

LESSONS = [
    "Планирование помогает достигать целей",
    "Маленькие шаги ведут к большим результатам",
    "Отдых так же важен, как и работа",
    "Благодарность меняет восприятие мира",
    "Фокус на важном приводит к успеху",
    "Последовательность - ключ к прогрессу",
    "Забота о себе повышает продуктивность",
    "Ошибки - это возможность для роста"
]

MOODS = ['great', 'good', 'normal', 'sad', 'bad']


def generate_entries(username, days=30):
    """Генерация тестовых записей за последние N дней"""

    # Получаем пользователя
    try:
        user = User.objects.get(username=username)
        print(f"✅ Пользователь найден: {username}")
    except User.DoesNotExist:
        print(f"❌ Пользователь {username} не найден!")
        print("Доступные пользователи:")
        for u in User.objects.all():
            print(f"  - {u.username}")
        return

    # Удаляем старые тестовые записи (опционально)
    old_entries = DiaryEntry.objects.filter(author=user)
    print(f"📊 У пользователя уже есть {old_entries.count()} записей")

    # Создаём новые записи
    created = 0
    for i in range(days, 0, -1):
        date = datetime.now().date() - timedelta(days=i)

        # Проверяем, есть ли уже запись за этот день
        if DiaryEntry.objects.filter(author=user, date=date).exists():
            print(f"⏭️  Пропускаем {date} - запись уже существует")
            continue

        # Случайный выбор данных
        morning_gratitude = "\n".join(random.sample(GRATITUDES, 3))
        morning_affirmation = random.choice(AFFIRMATIONS)
        morning_goals = "\n".join(random.sample(MORNING_GOALS, 2))
        evening_wins = "\n".join(random.sample(EVENING_WINS, 2))
        evening_improvement = random.choice(IMPROVEMENTS)
        evening_lesson = random.choice(LESSONS)
        mood = random.choice(MOODS)

        # Создаём запись
        entry = DiaryEntry.objects.create(
            author=user,
            date=date,
            morning_gratitude=morning_gratitude,
            morning_affirmation=morning_affirmation,
            morning_goals=morning_goals,
            evening_wins=evening_wins,
            evening_improvement=evening_improvement,
            evening_lesson=evening_lesson,
            mood=mood
        )
        created += 1
        print(f"✅ Создана запись за {date} (настроение: {mood})")

    print(f"\n🎉 Готово! Создано {created} новых записей за последние {days} дней")
    print(f"📊 Всего записей у пользователя: {DiaryEntry.objects.filter(author=user).count()}")


def show_statistics(username):
    """Показать статистику записей пользователя"""
    try:
        user = User.objects.get(username=username)
        entries = DiaryEntry.objects.filter(author=user)

        if not entries:
            print(f"📊 У пользователя {username} нет записей")
            return

        print(f"\n📊 СТАТИСТИКА ПОЛЬЗОВАТЕЛЯ {username.upper()}:")
        print(f"   Всего записей: {entries.count()}")
        print(f"   Первая запись: {entries.order_by('date').first().date}")
        print(f"   Последняя запись: {entries.order_by('-date').first().date}")

        # Статистика по настроению
        mood_stats = {}
        for mood in MOODS:
            count = entries.filter(mood=mood).count()
            if count > 0:
                mood_stats[mood] = count

        print(f"\n   📈 Распределение настроения:")
        mood_names = {
            'great': 'Отличное 🌟',
            'good': 'Хорошее 😊',
            'normal': 'Нормальное 😐',
            'sad': 'Грустное 😔',
            'bad': 'Плохое 😢'
        }
        for mood, count in mood_stats.items():
            print(f"      {mood_names.get(mood, mood)}: {count} раз ({count * 100 // entries.count()}%)")

    except User.DoesNotExist:
        print(f"❌ Пользователь {username} не найден!")


if __name__ == "__main__":
    print("=" * 50)
    print("🎯 ГЕНЕРАТОР ТЕСТОВЫХ ЗАПИСЕЙ")
    print("=" * 50)

    # Показать доступных пользователей
    print("\n📋 Доступные пользователи:")
    for user in User.objects.all():
        print(f"   - {user.username}")

    print("\n" + "=" * 50)

    # Запрашиваем имя пользователя
    username = input("\n👤 Введите имя пользователя (например, admin): ").strip()

    if not username:
        print("❌ Имя пользователя не может быть пустым!")
        exit()

    # Запрашиваем количество дней
    try:
        days = int(input("📅 Количество дней для генерации (например, 30): "))
    except ValueError:
        days = 30
        print(f"   Использую значение по умолчанию: {days} дней")

    print("\n" + "=" * 50)

    # Генерируем записи
    generate_entries(username, days)

    # Показать статистику
    show_statistics(username)

    print("\n" + "=" * 50)
    print("✨ Готово! Теперь у вас есть тестовые данные для демонстрации!")
    print("=" * 50)
