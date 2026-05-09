from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views_api

app_name = 'accounts_api'

urlpatterns = [
    path('register/', views_api.RegisterView.as_view(), name='register'),
    path('login/', views_api.LoginView.as_view(), name='login'),
    path('logout/', views_api.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views_api.ProfileView.as_view(), name='profile'),
    path('change-password/', views_api.ChangePasswordView.as_view(), name='change_password'),
]
