# Generated by Django 4.2.3 on 2024-04-16 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WBPMS', '0006_jemomedicine_selector'),
    ]

    operations = [
        migrations.AddField(
            model_name='lebumedicine',
            name='Selector',
            field=models.IntegerField(default=0),
        ),
    ]
