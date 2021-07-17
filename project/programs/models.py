from django.db import models
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
# Create your models here.
def upload_logo(instance, filename):
    extision = filename.split('.')[1]
    return 'programs/logos/%s.%s'%(instance.name,extision)

class Level(models.Model):
    name = models.CharField(max_length=80)
    point = models.FloatField()

    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')


    def __str__(self):
       return self.name



class Program(models.Model):
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="program" ,null=True, on_delete=models.SET_NULL)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_logo)
    url = models.URLField()
    policy = models.TextField()
    summery = models.TextField(blank=True)
    launch_date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    payings = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)


    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')


    def __str__(self):
       return self.company_name

class BountyBar(models.Model):
    program = OneToOneField(Program, related_name="bounty_bar", null=True, on_delete=models.SET_NULL)
    level = models.ForeignKey(Level, related_name="Bount", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=200)

class Asset(models.Model):
    url = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    paid = models.BooleanField(default=True)
    level = models.ForeignKey(Level, related_name='level_assets', on_delete=models.SET_NULL, null=True)
    reward = models.FloatField(blank=True)
    description = models.TextField(max_length=300)
    owner = models.ForeignKey('Program', related_name='program_assets', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')


    def __str__(self):
       return self.url
