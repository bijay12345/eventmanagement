# Generated by Django 4.1.4 on 2023-01-19 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0013_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_host', to='eventhost.eventhost'),
        ),
    ]
