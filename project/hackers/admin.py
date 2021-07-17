from django.contrib import admin
from .models import Hacker, Report, OWASP10, Skill, Session, Badge, Bounty,  Comment, Weakness

# Register your models here.

admin.site.register(Hacker)
admin.site.register(OWASP10)
admin.site.register(Skill)
admin.site.register(Report)
admin.site.register(Session)
admin.site.register(Badge)
admin.site.register(Bounty)
admin.site.register(Comment)
admin.site.register(Weakness)
