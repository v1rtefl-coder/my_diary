from django.urls import path
from . import views_api

app_name = 'entries_api'

urlpatterns = [
    path('', views_api.DiaryEntryListCreateView.as_view(), name='list_create'),
    path('<int:pk>/', views_api.DiaryEntryDetailView.as_view(), name='detail'),
    path('<int:pk>/morning/', views_api.MorningEntryView.as_view(), name='morning'),
    path('<int:pk>/evening/', views_api.EveningEntryView.as_view(), name='evening'),
    path('statistics/', views_api.EntryStatisticsView.as_view(), name='statistics'),
]
