# Generated by Django 3.0.3 on 2020-02-19 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drunk', '0002_auto_20200218_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cocktail',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='cocktail',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='cocktailreview',
            old_name='cocktail_id',
            new_name='cocktail',
        ),
        migrations.RenameField(
            model_name='cocktailreview',
            old_name='user_id',
            new_name='user',
        ),
    ]
