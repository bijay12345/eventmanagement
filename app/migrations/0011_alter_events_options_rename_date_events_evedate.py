# Generated by Django 4.1.4 on 2023-01-07 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_rating_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='events',
            options={'ordering': ['evedate']},
        ),
        migrations.RenameField(
            model_name='events',
            old_name='date',
            new_name='evedate',
        ),
    ]
