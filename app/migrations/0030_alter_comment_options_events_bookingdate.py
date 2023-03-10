# Generated by Django 4.1.4 on 2023-01-22 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_rename_customer_events_customers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date_commented']},
        ),
        migrations.AddField(
            model_name='events',
            name='bookingdate',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
