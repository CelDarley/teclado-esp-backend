from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.status_view, name='status'),
    path('check-auth/', views.check_auth_view, name='check_auth'),
    path('login/', views.login_view, name='login'),
    path('access/verify/', views.access_verify_view, name='access_verify'),
    path('users/', views.users_view, name='users'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    path('logs/', views.logs_view, name='logs'),
] 