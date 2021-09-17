# Generated by Django 3.1.7 on 2021-09-15 15:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hackers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(max_length=250)),
                ('message', models.TextField(max_length=250)),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'Badge',
                'verbose_name_plural': 'Badges',
            },
        ),
        migrations.CreateModel(
            name='Hacker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avater', models.ImageField(blank=True, null=True, upload_to=hackers.models.upload_avater)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('github', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('account', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hacker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hacker',
                'verbose_name_plural': 'Hackers',
            },
        ),
        migrations.CreateModel(
            name='OWASP10',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'OWASP10',
                'verbose_name_plural': 'OWASP10s',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Point',
                'verbose_name_plural': 'Points',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('triage_state', models.CharField(blank=True, choices=[('accepted', 'ACCEPTED'), ('rejected', 'REJECTED'), ('reviewing', 'REVIEWING')], default='reviewing', max_length=100)),
                ('open_state', models.CharField(blank=True, choices=[('processing', 'PROCESSING'), ('need more info', 'NEED MORE INFO'), ('done', 'DONE')], default='processing', max_length=100)),
                ('close_state', models.CharField(blank=True, choices=[('informative', 'INFORMATIVE'), ('resolved', 'RESOLVED'), ('duplicated', 'DUPLICATED'), ('spam', 'SPAM')], max_length=100)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('closed_at', models.DateTimeField(auto_now_add=True)),
                ('visibale', models.BooleanField(default=False)),
                ('asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_reports', to='programs.asset')),
                ('contributors', models.ManyToManyField(related_name='reports', to=settings.AUTH_USER_MODEL)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='level_reports', to='programs.level')),
                ('owasp10', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owasp10_reports', to='hackers.owasp10')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='hackers.hacker')),
                ('reported_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='our_reports', to='programs.program')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='Weakness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Weakness',
                'verbose_name_plural': 'Weaknesses',
            },
        ),
        migrations.CreateModel(
            name='TimeLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='time_line', to='hackers.report')),
            ],
        ),
        migrations.CreateModel(
            name='ReportAttachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to=hackers.models.upload_attachment)),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attachments', to='hackers.report')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='weakness',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weakness_reports', to='hackers.weakness'),
        ),
        migrations.CreateModel(
            name='HackerSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10)])),
                ('hacker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hacker_skills', to='hackers.hacker')),
                ('skill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skill_hackers', to='hackers.skill')),
            ],
        ),
        migrations.CreateModel(
            name='HackerPrefrences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hacker', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prefrences', to='hackers.hacker')),
            ],
        ),
        migrations.CreateModel(
            name='HackerPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('valid', models.BooleanField()),
                ('hacker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_points', to='hackers.hacker')),
                ('point', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hacker_points', to='hackers.point')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='our_points', to='programs.program')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='points', to='hackers.report')),
            ],
        ),
        migrations.CreateModel(
            name='HackerBadges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('giving_date', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='badge_hackers', to='hackers.badge')),
                ('hacker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hacker_badges', to='hackers.hacker')),
            ],
        ),
        migrations.AddField(
            model_name='hacker',
            name='badges',
            field=models.ManyToManyField(blank=True, related_name='badges_hacker', through='hackers.HackerBadges', to='hackers.Badge'),
        ),
        migrations.AddField(
            model_name='hacker',
            name='points',
            field=models.ManyToManyField(related_name='programs', through='hackers.HackerPoint', to='hackers.Point'),
        ),
        migrations.AddField(
            model_name='hacker',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='hackers', through='hackers.HackerSkills', to='hackers.Skill'),
        ),
        migrations.AddField(
            model_name='hacker',
            name='thankers',
            field=models.ManyToManyField(blank=True, related_name='thanked_hackers', to='programs.Program'),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verb', models.CharField(blank=True, choices=[('comment', 'Comment'), ('set_award', 'Set Award'), ('change_level', 'Change Level'), ('change_status', 'Change Status'), ('close', 'Close'), ('call_admin', 'Call Admin')], max_length=150)),
                ('level', models.CharField(blank=True, choices=[(1, 'none'), (2, 'low'), (3, 'medium'), (4, 'hight'), (5, 'critical')], max_length=150, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('open_state', models.CharField(blank=True, choices=[('processing', 'PROCESSING'), ('need more info', 'NEED MORE INFO'), ('done', 'DONE')], max_length=100, null=True)),
                ('close_state', models.CharField(blank=True, choices=[('informative', 'INFORMATIVE'), ('resolved', 'RESOLVED'), ('duplicated', 'DUPLICATED'), ('spam', 'SPAM')], max_length=100, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to=settings.AUTH_USER_MODEL)),
                ('timeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='hackers.timeline')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Bounty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('valid', models.BooleanField()),
                ('payer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='our_bounties', to='programs.program')),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_bounties', to='hackers.hacker')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Bounties', to='hackers.report')),
            ],
            options={
                'verbose_name': 'Bounty',
                'verbose_name_plural': 'Bounties',
            },
        ),
    ]
