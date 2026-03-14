from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('restore-password/', views.restore_password_view, name='restore-password'),
    path('verify-code/', views.verify_code_view, name='verify-code'),
]