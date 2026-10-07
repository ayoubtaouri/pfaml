from django.urls import path
from detection import views

app_name = 'detection'

urlpatterns = [
    path('', views.prediction_form, name='prediction_form'),
    path('result/<int:pk>/', views.prediction_result, name='prediction_result'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('delete/<int:pk>/', views.delete_prediction, name='delete_prediction'),
]
