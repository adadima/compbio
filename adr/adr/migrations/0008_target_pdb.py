# Generated by Django 2.2.7 on 2019-12-07 23:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0007_pocketmotif'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='pdb',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=[], size=None),
        ),
    ]
