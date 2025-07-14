from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.status_view, name='status'),
    path('check-auth/', views.check_auth_view, name='check_auth'),
    path('login/', views.login_view, name='login'),
    path('access/verify/', views.access_verify_view, name='access_verify'),
    
    # Device routes
    path('devices/', views.devices_view, name='devices'),
    path('devices/create/', views.create_device_view, name='create_device'),
    path('devices/<int:device_id>/delete/', views.delete_device_view, name='delete_device'),
    path('devices/<int:device_id>/update-ip/', views.update_device_ip_view, name='update_device_ip'),
    
    # User routes (now device-specific)
    path('users/', views.users_view, name='users'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    
    # Logs route (now device-specific)
    path('logs/', views.logs_view, name='logs'),
] 