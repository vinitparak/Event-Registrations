# Generated by Django 2.2.2 on 2019-12-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20191201_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privateevent',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='eventimages/'),
        ),
        migrations.AlterField(
            model_name='publicevent',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='eventimages/'),
        ),
    ]
