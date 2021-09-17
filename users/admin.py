from django.contrib import admin
from .models import  User
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from django.contrib.auth.models import Permission

# Register your models here.
#admin.site.register(Role)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "phone_number")
    list_filter = ("email", "username", "phone_number")
    search_fields =("email", "username", "phone_number")
   

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)
admin.site.register(Permission)