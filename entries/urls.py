from django.urls import path
from . import views

app_name = 'entries'

urlpatterns = [
    path('', views.entry_list, name='list'),
    path('morning/', views.morning_entry, name='morning'),
    path('evening/<int:pk>/', views.evening_entry, name='evening'),
    path('<int:pk>/', views.entry_detail, name='detail'),
    path('<int:pk>/delete/', views.entry_delete, name='delete'),
    path('statistics/', views.statistics, name='statistics'),
]
