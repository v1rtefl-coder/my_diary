from rest_framework import serializers
from .models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = DiaryEntry
        fields = (
            'id', 'date', 'author', 'author_username', 'author_email',
            'morning_gratitude', 'morning_affirmation', 'morning_goals',
            'evening_wins', 'evening_improvement', 'evening_lesson',
            'mood', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at', 'date')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class DiaryEntryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = ('id', 'date', 'mood', 'created_at')
