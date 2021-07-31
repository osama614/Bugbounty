from django.contrib import admin
from .models import Hacker, Report, OWASP10, Skill, Badge, Bounty,  Comment, Weakness, Point


# Register your models here.

admin.site.register(Hacker)
admin.site.register(OWASP10)
admin.site.register(Skill)
admin.site.register(Report)
admin.site.register(Badge)
admin.site.register(Bounty)
admin.site.register(Comment)
admin.site.register(Weakness)
admin.site.register(Point)

