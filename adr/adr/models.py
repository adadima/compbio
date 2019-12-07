from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Feature(models.Model):
    pass


class Drug(models.Model):
    drugbank_id = models.CharField(max_length=50, null=True)
    cid = models.CharField(max_length=50, null=True)
    smiles = models.CharField(max_length=10000, null=True)
    status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"Drug - cid: {self.cid}"


class Indication(Feature):
    indication_id = models.CharField(max_length=50)
    indication_name = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return f"Indication - id: {self.indication_id}, name: {self.indication_name}"


class Target(Feature):
    uniprot = models.CharField(max_length=50)
    pdb = ArrayField(models.CharField(max_length=50), default=list())
    protein_pocket_sequence = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return f"Protein Target - uniprot: {self.uniprot}"


class PocketMotif(Feature):
    motif_id = models.IntegerField()
    proteins = ArrayField(models.CharField(max_length=50))

    def __str__(self):
        return f"Protein pocket motif - id: {self.motif_id}"


class ADR(Feature):
    adr_id = models.CharField(max_length=50)
    adr_description = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return f"ADR - id: {self.adr_id}, descr: {self.adr_description}"


class SubStructure(Feature):
    struct_id = models.CharField(max_length=50)

    def __str__(self):
        return f"SubStructure - id: {self.struct_id}"


class Edge(models.Model):
    edge_type = models.CharField(max_length=50)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, default="-1")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True, default="-1")
    weight_value = models.FloatField(null=True)
    weight_units = models.CharField(max_length=50, null=True)
    weight_measure = models.CharField(max_length=50, null=True)
