# Generated by Django 4.2.3 on 2024-03-17 13:07

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('WBPMS', '0003_jemomedicine'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True),
        ),
    ]
