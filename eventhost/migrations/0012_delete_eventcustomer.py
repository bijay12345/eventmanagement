# Generated by Django 4.1.4 on 2023-01-17 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0011_alter_eventcustomer_customers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventCustomer',
        ),
    ]