# Generated by Django 4.1.4 on 2023-01-21 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0020_hostfeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostfeedback',
            name='eventhost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_feedback', to='eventhost.eventhost'),
        ),
    ]