# Generated by Django 2.2.2 on 2019-12-01 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20191201_1640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicevent',
            old_name='event_date',
            new_name='date',
        ),
    ]