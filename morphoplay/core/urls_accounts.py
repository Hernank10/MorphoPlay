from django.urls import path
from . import views as views_accounts

app_name = 'accounts'

urlpatterns = [
    path('register/', views_accounts.register, name='register'),
    path('login/', views_accounts.login_view, name='login'),
    path('logout/', views_accounts.logout_view, name='logout'),
    path('profile/', views_accounts.profile, name='profile'),
    path('profile/edit/', views_accounts.edit_profile, name='edit_profile'),
    path('password/change/', views_accounts.change_password, name='change_password'),
]
