from .serializers import AdSerializer
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Ad

# Create your views here.


class AdView(generics.ListCreateAPIView):
    serializer_class = AdSerializer
    #permission_classes = [IsAuthenticated]
    def get_queryset(self):

        return Ad.objects.filter(is_active=True).all()[:5]

class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdSerializer
   # permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'pk'
    def get_queryset(self):

        return Ad.objects.filter(is_active=True).all()[:5]
