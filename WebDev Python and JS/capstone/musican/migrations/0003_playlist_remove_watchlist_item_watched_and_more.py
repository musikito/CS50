# Generated by Django 4.1.3 on 2022-12-10 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musican', '0002_alter_songinfo_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_added', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_added', to='musican.songinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='item_watched',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.AlterField(
            model_name='categorylist',
            name='cat_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_name', to='musican.songinfo'),
        ),
        migrations.DeleteModel(
            name='Auction_listings',
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]