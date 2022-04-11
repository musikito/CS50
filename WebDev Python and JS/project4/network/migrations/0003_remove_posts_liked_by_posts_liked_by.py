# Generated by Django 4.0.3 on 2022-04-11 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='posts',
            name='liked_by',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
