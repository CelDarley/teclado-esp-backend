from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_connection, name='test_connection'),
    path('keyboard/status/', views.keyboard_status, name='keyboard_status'),
] 