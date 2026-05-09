from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import DiaryEntry
from .forms import MorningEntryForm, EveningEntryForm, SearchForm
from datetime import date


@login_required
def entry_list(request):
    """Список всех записей"""
    entries = DiaryEntry.objects.filter(author=request.user)
    form = SearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            entries = entries.filter(
                Q(morning_gratitude__icontains=query) |
                Q(morning_affirmation__icontains=query) |
                Q(morning_goals__icontains=query) |
                Q(evening_wins__icontains=query) |
                Q(evening_improvement__icontains=query) |
                Q(evening_lesson__icontains=query)
            )

    # Статистика
    total_entries = entries.count()
    completed_morning = entries.filter(morning_gratitude__isnull=False).count()
    completed_evening = entries.filter(evening_wins__isnull=False).count()

    # Текущая запись за сегодня
    today_entry = DiaryEntry.objects.filter(author=request.user, date=date.today()).first()

    return render(request, 'entries/list.html', {
        'entries': entries,
        'form': form,
        'total_entries': total_entries,
        'completed_morning': completed_morning,
        'completed_evening': completed_evening,
        'today_entry': today_entry,
    })


@login_required
def entry_detail(request, pk):
    """Детальный просмотр записи"""
    entry = get_object_or_404(DiaryEntry, pk=pk, author=request.user)
    return render(request, 'entries/detail.html', {'entry': entry})


@login_required
def morning_entry(request):
    """Утренняя запись (3 минуты)"""
    today_entry, created = DiaryEntry.objects.get_or_create(
        author=request.user,
        date=date.today()
    )

    # Если утренняя часть уже заполнена
    if today_entry.morning_gratitude and today_entry.morning_affirmation and today_entry.morning_goals:
        messages.info(request, '✨ Утренняя часть уже заполнена на сегодня!')
        return redirect('entries:evening', pk=today_entry.pk)

    if request.method == 'POST':
        form = MorningEntryForm(request.POST, instance=today_entry)
        if form.is_valid():
            form.save()
            messages.success(request, '🌟 Отличное начало дня! Вечером вас ждёт 3-минутный обзор.')
            return redirect('entries:list')
    else:
        form = MorningEntryForm(instance=today_entry)

    return render(request, 'entries/morning_form.html', {
        'form': form,
        'title': '🌅 Доброе утро! 3 минуты для настройки на успех'
    })


@login_required
def evening_entry(request, pk):
    """Вечерняя запись (3 минуты)"""
    entry = get_object_or_404(DiaryEntry, pk=pk, author=request.user)

    # Проверяем, заполнена ли утренняя часть
    if not entry.morning_gratitude:
        messages.warning(request, 'Сначала заполните утреннюю часть дневника!')
        return redirect('entries:morning')

    if request.method == 'POST':
        form = EveningEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, '🎉 Отличный день! Вы сделали большой шаг к своей лучшей версии!')
            return redirect('entries:list')
    else:
        form = EveningEntryForm(instance=entry)

    return render(request, 'entries/evening_form.html', {
        'form': form,
        'title': '🌙 Добрый вечер! 3 минуты для подведения итогов',
        'entry': entry
    })


@login_required
def entry_delete(request, pk):
    """Удаление записи"""
    entry = get_object_or_404(DiaryEntry, pk=pk, author=request.user)

    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Запись удалена')
        return redirect('entries:list')

    return render(request, 'entries/confirm_delete.html', {'entry': entry})


@login_required
def statistics(request):
    """Статистика успеха"""
    entries = DiaryEntry.objects.filter(author=request.user)

    # Статистика по настроению
    mood_stats = {}
    for mood_choice in DiaryEntry._meta.get_field('mood').choices:
        mood_code = mood_choice[0]
        count = entries.filter(mood=mood_code).count()
        mood_stats[mood_choice[1]] = count

    # Топ слов в благодарностях
    all_gratitude = ' '.join(entries.values_list('morning_gratitude', flat=True))

    context = {
        'total_days': entries.count(),
        'mood_stats': mood_stats,
        'streak': calculate_streak(entries),
        'total_wins': sum(len(e.evening_wins.split('\n')) for e in entries if e.evening_wins),
    }

    return render(request, 'entries/statistics.html', context)


def calculate_streak(entries):
    """Расчет непрерывной серии записей"""
    if not entries:
        return 0

    dates = sorted(entries.values_list('date', flat=True))
    streak = 1
    max_streak = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    return max_streak
