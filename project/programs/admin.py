from django.contrib import admin
from .models import Program , Level, Asset, BountyBar, Announcement
# Register your models here.

admin.site.register(Program )
admin.site.register(Level)
admin.site.register(Asset)
admin.site.register(BountyBar)
admin.site.register(Announcement)

