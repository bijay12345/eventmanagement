# Generated by Django 4.1.4 on 2023-01-17 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventhost', '0005_rename_host_name_eventhost_management_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('functionname', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('contact', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('date', models.DateField()),
                ('managingfirm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventhost.eventhost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
