# Generated by Django 5.1.3 on 2024-11-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0003_light'),
    ]

    operations = [
        migrations.AddField(
            model_name='light',
            name='transition_time',
            field=models.IntegerField(null=True),
        ),
    ]