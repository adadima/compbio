from django.db import models


class Feature(models.Model):
    feature_id = models.CharField(max_length=50)


class Drug(models.Model):
    drugbank_id = models.CharField(max_length=50)
    smiles = models.CharField(max_length=10000)


class Indication(Feature):
    pass


class Target(Feature):
    protein_pocket_sequence = models.CharField(max_length=10000, null=True)


class ADR(Feature):
    pass


class SubStructure(Feature):
    pass


class Edge(models.Model):
    edge_type = models.CharField(max_length=50)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
    weight_value = models.FloatField(null=True)
    weight_units = models.CharField(max_length=50, null=True)


