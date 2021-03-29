# Generated by Django 3.1.5 on 2021-03-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_auto_20210329_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='films',
        ),
        migrations.AddField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(to='films.Genre'),
        ),
    ]
