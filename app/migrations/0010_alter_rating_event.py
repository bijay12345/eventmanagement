# Generated by Django 4.1.4 on 2023-01-07 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_rating_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.events'),
        ),
    ]
