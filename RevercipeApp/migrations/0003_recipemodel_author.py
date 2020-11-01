# Generated by Django 3.1.2 on 2020-10-31 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RevercipeApp', '0002_auto_20201030_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipemodel',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
