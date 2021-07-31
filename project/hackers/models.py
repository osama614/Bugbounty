
from django.db import models
from django.conf import settings
from programs.models import Level, Program, Asset
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

user = get_user_model()

def upload_avater(instance, filename):
    extision = filename.split('.')[1]
    return 'hackers/avaters/' + filename 

def upload_attachment(instance, filename):
    extision = filename.split('.')[1]
    return 'hackers/reports/attachments/%s.%s'%(instance.title,extision)

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=80)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(10)])

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')


    def __str__(self):
       return self.name

class Badge(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=250)
    image = models.ImageField()

    class Meta:
        verbose_name = _('Badge')
        verbose_name_plural = _('Badges')


    def __str__(self):
       return self.name


class Weakness(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = _('Weakness')
        verbose_name_plural = _('Weaknesses')


    def __str__(self):
       return self.name

class OWASP10(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('OWASP10')
        verbose_name_plural = _('OWASP10s')


    def __str__(self):
       return self.name

class Comment(models.Model):
    body = models.TextField()
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments" ,null=True, on_delete=models.SET_NULL)
    #report = models.ForeignKey(Report, related_name="comments" ,null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


    def __str__(self):
       return f"comment by {self.owner.username}"

class Report(models.Model):
    TRIAGE_STATES = (
                        ('accepted', "ACCEPTED"),
                        ('rejected',"REJECTED"),
                        ('reviewing', "REVIEWING"),
                    )
    OPEN_STATES = (
                    ('processing', "PROCESSING"),
                    ('need more info', "NEED MORE INFO"),
                    ("done", "DONE")
                  )

    CLOSE_STATES = (
                    ("informative", "INFORMATIVE"),
                    ("resolved","RESOLVED"),
                    ("duplicated", "DUPLICATED"),
                    ("spam", "SPAM")
                  )

    title = models.CharField(max_length=150)
    description = models.TextField()
    triage_state = models.CharField(choices=TRIAGE_STATES, default='reviewing', max_length=100, blank=True)
    open_state = models.CharField(choices=OPEN_STATES, default='processing', max_length=100, blank=True)
    close_state = models.CharField(choices=CLOSE_STATES, max_length=100, blank=True)
    #attachment = models.FileField(upload_to=upload_attachment)
    video = models.TextField()
    level = models.ForeignKey(Level, related_name="level_reports" ,null=True, on_delete=models.SET_NULL)
    weakness = models.ForeignKey(Weakness, related_name="weakness_reports" ,null=True, on_delete=models.SET_NULL)
    owasp10 = models.ForeignKey(OWASP10, related_name="owasp10_reports" ,null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey('Hacker', related_name="reports" ,null=True, on_delete=models.SET_NULL)
    asset = models.ForeignKey(Asset, related_name="asset_reports" ,null=True, on_delete=models.SET_NULL)
    reported_to = models.ForeignKey(Program, related_name="our_reports" ,null=True, on_delete=models.SET_NULL)
    comments = models.ForeignKey(Comment, related_name="reports", blank=True ,null=True, on_delete=models.SET_NULL)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(auto_now_add=True)
    bounty = models.ForeignKey("Bounty", related_name="reports", blank=True ,null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')


    def __str__(self):
       return self.title

class ReportAttachments(models.Model):
    path = models.FileField(upload_to=upload_attachment)
    report = models.ForeignKey(Report, related_name="attachments" ,null=True, on_delete=models.SET_NULL)

class Hacker(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="hacker" ,null=True, on_delete=models.SET_NULL)
    skills = models.ManyToManyField(Skill, related_name="hackers" ,blank=True)
    badges = models.ManyToManyField(Badge, related_name="badges_hacker" ,blank=True)
    avater = models.ImageField(blank=True, upload_to=upload_avater, null=True)
    rank = models.IntegerField(blank=True, null=True)
    points = models.ManyToManyField(Program, through='Point', related_name='programs')
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    thankers = models.ManyToManyField(Program, related_name="thanked_hackers" ,blank=True)
    earnings = models.ManyToManyField(Program, through='Bounty', related_name='payers')



    class Meta:
        verbose_name = _('Hacker')
        verbose_name_plural = _('Hackers')

    def __str__(self):
       return self.account.username

class HackerPrefrences(models.Model):
    pass

class Bounty(models.Model):
    amount = models.FloatField()
    payer = models.ForeignKey(Program, related_name="our_bounties" ,blank=True, on_delete=models.SET_NULL, null=True)
    recipient = models.ForeignKey(Hacker, related_name="my_bounties" ,blank=True, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField()

    class Meta:
        verbose_name = _('Bounty')
        verbose_name_plural = _('Bounties')


    def __str__(self):
       return f"Bounty {self.payer.company_name} to {self.recipient}"

class Point(models.Model):
    amount = models.IntegerField(default=0)
    program = models.ForeignKey(Program, related_name="our_points" ,blank=True, on_delete=models.SET_NULL, null=True)
    hacker = models.ForeignKey(Hacker, related_name="my_points" ,blank=True, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField()

    class Meta:
        verbose_name = _('Point')
        verbose_name_plural = _('Points')

    def __str__(self):
       return f"Point from {self.program.company_name } to {self.hacker}"

