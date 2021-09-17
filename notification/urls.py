from django.urls import path

from . import views

urlpatterns = [
    path('', views.NotificationView.as_view(), name='live_notifications'),
    path('home', views.index, name='index'),
    path('home/<str:room_name>/', views.room, name='room'),
]