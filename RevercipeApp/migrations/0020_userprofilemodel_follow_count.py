# Generated by Django 3.1.2 on 2020-11-30 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RevercipeApp', '0019_auto_20201116_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='follow_count',
            field=models.IntegerField(default=0),
        ),
    ]
