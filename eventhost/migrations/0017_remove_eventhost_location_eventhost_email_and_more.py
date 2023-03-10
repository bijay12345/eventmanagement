# Generated by Django 4.1.4 on 2023-01-21 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0016_eventhost_image_delete_hostimages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventhost',
            name='location',
        ),
        migrations.AddField(
            model_name='eventhost',
            name='email',
            field=models.EmailField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='phonenumber',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='pincode',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='state',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
