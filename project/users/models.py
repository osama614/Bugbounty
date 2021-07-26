from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField



# Create your models here

# class Role(models.Model):
#     name = models.CharField(max_length=20)


#     class Meta:
#         verbose_name = _('Role')
#         verbose_name_plural = _('Roles')


#     def __str__(self):
#        return self.name


class User(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    HACKER = 'hacker'
    PROGRAM = 'program'
      
    ROLE_CHOICES = (
          (ADMIN, 'Admin'),
          (STAFF, 'Staff'),
          (HACKER, 'Hacker'),
          (PROGRAM, 'Program')
      )
      
    GENDER_CHOICES = (('male', "Male"),
              ("female", "Female"))
    bio = models.TextField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True)
    phone_number = PhoneNumberField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100, blank=True)
    verified_email = models.BooleanField(default=False)
    verified_phone = models.BooleanField(default=False)
    accept_rules = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    role = models.CharField(choices=ROLE_CHOICES,max_length=80, blank=True, null=True)
    #role = models.ManyToManyField("Role")



