# Generated by Django 4.0.3 on 2022-05-23 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts_currentuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='currentuser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currentuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
