# Generated by Django 3.1.2 on 2020-10-16 16:57

import RevercipeApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=800)),
                ('rating', RevercipeApp.models.IntegerRangeField()),
            ],
        ),
        migrations.CreateModel(
            name='IngredientModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
                ('units', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('comments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='RevercipeApp.comment')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RevercipeApp.comment')),
                ('django_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pantry_ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RevercipeApp.ingredientmodel')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RevercipeApp.recipemodel')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientmodel',
            name='nutrients',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='RevercipeApp.nutrients'),
        ),
        migrations.AddField(
            model_name='ingredientmodel',
            name='recipes',
            field=models.ManyToManyField(to='RevercipeApp.RecipeModel'),
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('recipes', models.ManyToManyField(to='RevercipeApp.RecipeModel')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('follower', 'following')},
            },
        ),
    ]
