from django.urls import path
from admin_panel import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('users/<int:user_id>/export/', views.export_user_history, name='export_user_history'),
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('predictions/<int:prediction_id>/delete/', views.admin_delete_prediction, name='admin_delete_prediction'),
]
