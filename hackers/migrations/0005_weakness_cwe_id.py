# Generated by Django 3.1.7 on 2021-09-22 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0004_bounty_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='weakness',
            name='cwe_id',
            field=models.IntegerField(default=2, unique=True),
            preserve_default=False,
        ),
    ]