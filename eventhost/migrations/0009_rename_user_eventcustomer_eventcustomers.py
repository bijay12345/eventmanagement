# Generated by Django 4.1.4 on 2023-01-17 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0008_alter_eventcustomer_managingfirm_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventcustomer',
            old_name='user',
            new_name='eventcustomers',
        ),
    ]