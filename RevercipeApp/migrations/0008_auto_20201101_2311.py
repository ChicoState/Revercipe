# Generated by Django 3.1.2 on 2020-11-01 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RevercipeApp', '0007_auto_20201101_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='django_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
