# Generated by Django 3.1.2 on 2020-11-07 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RevercipeApp', '0009_auto_20201101_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='recipes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='RevercipeApp.recipemodel'),
        ),
    ]
