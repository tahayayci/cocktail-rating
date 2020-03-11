# Generated by Django 3.0.3 on 2020-02-17 13:24

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
            name='Cocktail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('is_alcoholoic', models.BooleanField()),
                ('cocktail_recipe', models.CharField(max_length=256)),
                ('cocktail_picture', models.ImageField(upload_to='')),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CocktailGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='CocktailReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taste_star', models.PositiveSmallIntegerField()),
                ('cost_star', models.PositiveSmallIntegerField()),
                ('prep_hardness_star', models.PositiveSmallIntegerField()),
                ('notes', models.TextField()),
                ('cocktail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drunk.Cocktail')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cocktail',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drunk.CocktailGroup'),
        ),
        migrations.AddField(
            model_name='cocktail',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
