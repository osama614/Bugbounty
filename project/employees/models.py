# from django.db import models
# from django.conf import settings
# from django.utils.translation import gettext_lazy as _
# # Create your models here.

# def upload_avater(instance, filename):
#     extision = filename.split('.')[1]
#     return 'employees/avaters/%s.%s'%(instance.account.username,extision)


# class Employee(models.Model):
#     account = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="employee" ,null=True, on_delete=models.SET_NULL)
#     avater = models.ImageField(blank=True, upload_to=upload_avater)

#     class Meta:
#         verbose_name = _('Employee')
#         verbose_name_plural = _('Employees')


#     def __str__(self):
#        return self.account.username