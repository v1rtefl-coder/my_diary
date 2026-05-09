from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import date


class DiaryEntry(models.Model):
    """Модель записи дневника в стиле 6-минутного дневника"""

    # Дата записи - добавлен default
    date = models.DateField('Дата', default=date.today)  # Изменено здесь

    # Остальные поля остаются без изменений
    morning_gratitude = models.TextField('За что я благодарен?',
                                         help_text='3-5 вещей за которые вы благодарны',
                                         blank=True)
    morning_affirmation = models.CharField('Моя аффирмация',
                                           max_length=500,
                                           help_text='Позитивное утверждение о себе',
                                           blank=True)
    morning_goals = models.TextField('Что сделает сегодняшний день великим?',
                                     help_text='2-3 ключевые задачи на день',
                                     blank=True)

    evening_wins = models.TextField('Мои сегодняшние победы',
                                    help_text='Чего я достиг сегодня?',
                                    blank=True)
    evening_improvement = models.TextField('Что я мог сделать лучше?',
                                           help_text='Уроки на сегодня',
                                           blank=True)
    evening_lesson = models.TextField('Чему я научился сегодня?',
                                      help_text='Новые инсайты и открытия',
                                      blank=True)

    mood = models.CharField('Настроение',
                            max_length=20,
                            choices=[
                                ('great', 'Отличное 🌟'),
                                ('good', 'Хорошее 😊'),
                                ('normal', 'Нормальное 😐'),
                                ('sad', 'Грустное 😔'),
                                ('bad', 'Плохое 😢'),
                            ],
                            default='normal')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Автор'
    )

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Запись в дневнике успеха'
        verbose_name_plural = 'Записи в дневнике успеха'
        ordering = ['-date']
        unique_together = ['author', 'date']  # Только одна запись в день

    def __str__(self):
        return f"Дневник успеха - {self.date}"

    def get_absolute_url(self):
        return reverse('entries:detail', kwargs={'pk': self.pk})

    def get_morning_completed(self):
        """Проверяет, заполнена ли утренняя часть"""
        return bool(self.morning_gratitude and self.morning_affirmation and self.morning_goals)

    def get_evening_completed(self):
        """Проверяет, заполнена ли вечерняя часть"""
        return bool(self.evening_wins and self.evening_improvement and self.evening_lesson)
