from django.urls import path
from .views import AdView, AdDetailView

app_name = "ads"
urlpatterns = [
    path('', AdView.as_view(), name='ads'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    
]