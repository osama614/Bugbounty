from django.contrib import admin
from .models import Hacker, Report, OWASP10, Skill, Badge, Bounty, Weakness, Point, HackerSkills, HackerBadges, TimeLine, HackerPoint, Event, HackerPrefrences


# Register your models here.

admin.site.register(Hacker)
admin.site.register(OWASP10)
admin.site.register(Skill)
admin.site.register(Report)
admin.site.register(Badge)
admin.site.register(Bounty)
# admin.site.register(Comment)
admin.site.register(Weakness)
admin.site.register(Point)
admin.site.register(HackerSkills)
admin.site.register(HackerBadges)
admin.site.register(TimeLine)
admin.site.register(HackerPoint)
admin.site.register(Event)
admin.site.register(HackerPrefrences)