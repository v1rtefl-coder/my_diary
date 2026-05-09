from django.contrib import admin
from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'author', 'get_morning_status', 'get_evening_status', 'mood']
    list_filter = ['date', 'mood', 'author']
    search_fields = ['morning_gratitude', 'morning_affirmation', 'morning_goals',
                     'evening_wins', 'evening_improvement', 'evening_lesson']
    list_per_page = 20
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Информация о записи', {
            'fields': ('author', 'date', 'mood')
        }),
        ('🌅 Утренняя часть (3 минуты)', {
            'fields': ('morning_gratitude', 'morning_affirmation', 'morning_goals'),
            'classes': ('wide',),
        }),
        ('🌙 Вечерняя часть (3 минуты)', {
            'fields': ('evening_wins', 'evening_improvement', 'evening_lesson'),
            'classes': ('wide',),
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_morning_status(self, obj):
        """Статус утренней части"""
        if obj.morning_gratitude and obj.morning_affirmation and obj.morning_goals:
            return '✅ Заполнено'
        return '❌ Не заполнено'

    get_morning_status.short_description = 'Утро'
    get_morning_status.admin_order_field = 'morning_gratitude'

    def get_evening_status(self, obj):
        """Статус вечерней части"""
        if obj.evening_wins and obj.evening_improvement and obj.evening_lesson:
            return '✅ Заполнено'
        return '❌ Не заполнено'

    get_evening_status.short_description = 'Вечер'
    get_evening_status.admin_order_field = 'evening_wins'

    actions = ['mark_morning_completed', 'mark_evening_completed']

    def mark_morning_completed(self, request, queryset):
        """Отметить утреннюю часть как заполненную"""
        updated = queryset.update(
            morning_gratitude='Благодарность за этот день',
            morning_affirmation='Я становлюсь лучше каждый день',
            morning_goals='Сделать этот день продуктивным'
        )
        self.message_user(request, f'{updated} записей обновлено (утренняя часть)')

    mark_morning_completed.short_description = 'Отметить утро как заполненное'

    def mark_evening_completed(self, request, queryset):
        """Отметить вечернюю часть как заполненную"""
        updated = queryset.update(
            evening_wins='Я справился с задачами дня',
            evening_improvement='Можно быть более продуктивным',
            evening_lesson='Каждый день - это возможность для роста'
        )
        self.message_user(request, f'{updated} записей обновлено (вечерняя часть)')

    mark_evening_completed.short_description = 'Отметить вечер как заполненный'
