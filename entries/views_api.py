from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer, DiaryEntryListSerializer


class DiaryEntryListCreateView(generics.ListCreateAPIView):
    """Список записей и создание новой"""
    serializer_class = DiaryEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['morning_gratitude', 'morning_affirmation', 'morning_goals',
                     'evening_wins', 'evening_improvement', 'evening_lesson']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DiaryEntryListSerializer
        return DiaryEntrySerializer


class DiaryEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детальный просмотр, редактирование, удаление записи"""
    serializer_class = DiaryEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)


class MorningEntryView(generics.UpdateAPIView):
    """Обновление утренней части записи"""
    serializer_class = DiaryEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={
            'morning_gratitude': request.data.get('morning_gratitude'),
            'morning_affirmation': request.data.get('morning_affirmation'),
            'morning_goals': request.data.get('morning_goals'),
        }, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EveningEntryView(generics.UpdateAPIView):
    """Обновление вечерней части записи"""
    serializer_class = DiaryEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={
            'evening_wins': request.data.get('evening_wins'),
            'evening_improvement': request.data.get('evening_improvement'),
            'evening_lesson': request.data.get('evening_lesson'),
            'mood': request.data.get('mood'),
        }, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EntryStatisticsView(APIView):
    """Статистика записей"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        entries = DiaryEntry.objects.filter(author=request.user)

        # Статистика по настроению
        mood_stats = {}
        for mood_choice in DiaryEntry._meta.get_field('mood').choices:
            mood_code = mood_choice[0]
            count = entries.filter(mood=mood_code).count()
            mood_stats[mood_code] = count

        return Response({
            'total_entries': entries.count(),
            'mood_statistics': mood_stats,
            'morning_completed': entries.exclude(morning_gratitude='').count(),
            'evening_completed': entries.exclude(evening_wins='').count(),
        })
