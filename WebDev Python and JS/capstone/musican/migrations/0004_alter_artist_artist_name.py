# Generated by Django 4.0.3 on 2022-06-22 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musican', '0003_rename_name_artist_artist_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artist_name',
            field=models.CharField(max_length=14),
        ),
    ]
