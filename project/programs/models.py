#from project.hackers.serializers import User
from django.db import models
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
# Create your models here.
def upload_logo(instance, filename):
    extision = filename.split('.')[1]
    return 'programs/logos/%s.%s'%(instance.company_name,extision)

class Level(models.Model):
    name = models.CharField(max_length=80)
    point = models.FloatField()

    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')


    def __str__(self):
       return self.name



class Program(models.Model):
    STATUS_CHOICES = (

        ("opened", "Opened"),
        ("closed", "Closed"),
        ("eligable","Eligable")

    )
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="program" ,null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_logo)
    url = models.URLField()
    policy = models.TextField()
    summery = models.TextField(blank=True)
    launch_date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    payings = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    status =  models.CharField(max_length=100, choices=STATUS_CHOICES, default="opened")

    class Meta:
        verbose_name = _('Program')
        verbose_name_plural = _('Programs')


    def __str__(self):
       return self.company_name

class BountyBar(models.Model):
    program = models.ForeignKey(Program, related_name="bounty_bars", null=True, on_delete=models.SET_NULL)
    level = models.ForeignKey(Level, related_name="Bount", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, )
    def __str__(self):
       return f"{self.program.company_name} {self.level} Bounty"

class Asset(models.Model):
    TYPE_CHOICES = (
        ("dm","Domain Name"),
        ("ios","IOS"),
        ("android","Android"),
        ("windows", "Windows")
    )
    url = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="dm")
    paid = models.BooleanField(default=True)
    level = models.ForeignKey(Level, related_name='level_assets', on_delete=models.SET_NULL, null=True)
    reward = models.FloatField(blank=True)
    description = models.TextField(max_length=300)
    owner = models.ForeignKey('Program', related_name='program_assets', on_delete=models.SET_NULL, null=True)
    in_scope = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')


    def __str__(self):
       return self.url

class Announcement(models.Model):
    program = models.ForeignKey(Program, related_name="announcements", null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="announcements", null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(timezone.now())
    is_active = models.BooleanField()
    
    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')


    def __str__(self):
       return self.title