# Generated by Django 3.1.2 on 2020-11-16 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RevercipeApp', '0015_auto_20201116_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='favorite',
            field=models.IntegerField(default=0),
        ),
    ]
