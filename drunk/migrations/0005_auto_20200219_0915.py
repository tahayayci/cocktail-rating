# Generated by Django 3.0.3 on 2020-02-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drunk', '0004_auto_20200219_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocktail',
            name='picture',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
