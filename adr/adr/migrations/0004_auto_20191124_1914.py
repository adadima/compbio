# Generated by Django 2.2.7 on 2019-11-24 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0003_auto_20191120_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='substructure',
            old_name='str_id',
            new_name='struct_id',
        ),
        migrations.RenameField(
            model_name='target',
            old_name='target_id',
            new_name='uniprot',
        ),
        migrations.AddField(
            model_name='adr',
            name='adr_description',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='drug',
            name='cid',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='edge',
            name='weight_measure',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='indication',
            name='indication_name',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='target',
            name='protein_pocket_sequence',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='smiles',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='edge',
            name='drug',
            field=models.ForeignKey(default='-1', on_delete=django.db.models.deletion.CASCADE, to='adr.Drug'),
        ),
        migrations.AlterField(
            model_name='edge',
            name='feature_id',
            field=models.ForeignKey(default='-1', null=True, on_delete=django.db.models.deletion.CASCADE, to='adr.Feature'),
        ),
    ]