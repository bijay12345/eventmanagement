# Generated by Django 4.1.4 on 2023-01-07 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_rating_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.events'),
        ),
    ]
