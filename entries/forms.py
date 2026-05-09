from django import forms
from .models import DiaryEntry


class MorningEntryForm(forms.ModelForm):
    """Утренняя форма (3 минуты)"""

    class Meta:
        model = DiaryEntry
        fields = ['morning_gratitude', 'morning_affirmation', 'morning_goals']
        widgets = {
            'morning_gratitude': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '✨ За что я благодарен сегодня?\n1. ...\n2. ...\n3. ...'
            }),
            'morning_affirmation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Я - уверенный и успешный человек, который...'
            }),
            'morning_goals': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Что сделает сегодняшний день великим?\n✓ ...\n✓ ...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True


class EveningEntryForm(forms.ModelForm):
    """Вечерняя форма (3 минуты)"""

    class Meta:
        model = DiaryEntry
        fields = ['evening_wins', 'evening_improvement', 'evening_lesson', 'mood']
        widgets = {
            'evening_wins': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '🏆 Мои победы сегодня:\n✓ ...\n✓ ...\n✓ ...'
            }),
            'evening_improvement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Что я мог сделать лучше?\n• ...\n• ...'
            }),
            'evening_lesson': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Чему я научился сегодня?\n💡 ...'
            }),
            'mood': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True


class SearchForm(forms.Form):
    """Форма поиска записей"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '🔍 Поиск по записям...'
        })
    )
