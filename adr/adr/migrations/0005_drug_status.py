# Generated by Django 2.2.7 on 2019-11-24 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0004_auto_20191124_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
