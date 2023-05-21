# Generated by Django 4.1.4 on 2023-01-21 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0018_remove_eventhost_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventhost',
            name='city',
            field=models.CharField(default='siliguri', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='description',
            field=models.CharField(default='Not available', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='phonenumber',
            field=models.CharField(default='0000000000', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='pincode',
            field=models.CharField(default='888888', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='state',
            field=models.CharField(default='Not Available', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventhost',
            name='street',
            field=models.CharField(default='Not Available', max_length=100),
            preserve_default=False,
        ),
    ]
