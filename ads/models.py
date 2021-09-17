from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

def upload_ad(instance, filename):
    extision = filename.split('.')[1]
    return 'bugbounty/ads/%s%s.%s'%(instance.title, instance.id, extision)


class Ad(models.Model):
    title= models.CharField(blank=True, max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_ad)
    ad_link = models.URLField(blank=True)
    author = models.OneToOneField(User, related_name="ads", null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    upadated_date = models.DateTimeField(auto_now=True)