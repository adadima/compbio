# Generated by Django 2.2.7 on 2019-11-20 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0002_auto_20191119_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubStructure',
            fields=[
                ('feature_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='adr.Feature')),
                ('str_id', models.CharField(max_length=50)),
            ],
            bases=('adr.feature',),
        ),
        migrations.AlterField(
            model_name='edge',
            name='drug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adr.Drug'),
        ),
        migrations.AlterField(
            model_name='edge',
            name='feature_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adr.Feature'),
        ),
    ]
