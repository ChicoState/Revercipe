# Generated by Django 3.1.2 on 2020-12-01 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RevercipeApp', '0022_auto_20201130_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofilemodel',
            name='favorite_count',
        ),
        migrations.RemoveField(
            model_name='userprofilemodel',
            name='follower_count',
        ),
        migrations.RemoveField(
            model_name='userprofilemodel',
            name='following_count',
        ),
    ]