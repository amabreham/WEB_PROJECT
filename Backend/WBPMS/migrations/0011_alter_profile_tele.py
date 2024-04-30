# Generated by Django 4.2.3 on 2024-04-21 11:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WBPMS', '0010_alter_profile_tele'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tele',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+251?1?\\d{9,15}$'), django.core.validators.MaxLengthValidator]),
        ),
    ]