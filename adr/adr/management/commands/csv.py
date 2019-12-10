import os
import sys
import random
import csv

parent_dir = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__)
            ))))
sys.path.insert(1, parent_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adr.settings")
import django
django.setup()
from django.core.management.base import BaseCommand
from adr.models import *


class Command(BaseCommand):

    value_limits = {"Ki": 0, "Kd": 0, "IC50": 0}

    def handle(self, *args, **options):
        num_drugs = 1000 #int(args[0])
        csv_name = "./adr/management/commands/data/out/graph4.csv"
        drugs, ind_edges, adr_edges, struct_edges, target_edges = self.select_entries(num_drugs)

        with open(csv_name, 'w') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["drug", "source", "type", "destination", "other", "weight", "measure"])
            print("Wrote header column.")
            self.write_targets(writer, target_edges)
            print("Wrote targets")
            self.write_adrs(writer, adr_edges)
            print("Wrote adrs")
            self.write_indications(writer, ind_edges)
            print("Wrote indications")
            self.write_substructures(writer, struct_edges)
            print("Wrote substructures")

    def write_row(self, csv_writer, drug, source, type, destination, other, weight, measure):
        csv_writer.writerow([drug, source, type, destination, other, weight, measure])

    def write_targets(self, csv_file, target_edges):    # value limits maps a measure ( Ki, Kd, IC50 ) to an affinity threshold
        total = len(target_edges)
        count = 0
        for edge in target_edges:
            if edge.weight_value < self.value_limits[edge.weight_measure]:
                continue
            self.write_row(csv_file, edge.drug.cid,
                           "DRUG", "DRUG_TARGETS", "TARGET",
                           edge.feature.id,
                           str(edge.weight_value),
                           edge.weight_measure)
            count += 1
            # print(f"{count} / {total} targets done")

    def write_adrs(self, csv_file, adr_edges):
        total = len(adr_edges)
        count = 0
        for edge in adr_edges:
            self.write_row(csv_file, edge.drug.cid, "DRUG", "HAS_SIDE_EFFECT", "SIDEFFECT",
                           edge.feature.id, "1",  "")

            count += 1
            # print(f"{count} / {total} adrs done")

    def write_indications(self, csv_file, ind_edges):
        total = len(ind_edges)
        count = 0
        for edge in ind_edges:
            self.write_row(csv_file, edge.drug.cid, "DRUG", "INDICATED_FOR", "INDICATION",
                           edge.feature.id, "1",  "")

            count += 1
            # print(f"{count} / {total} indications done")

    def write_substructures(self, csv_file, struct_edges):
        total = len(struct_edges)
        count = 0
        for edge in struct_edges:
            self.write_row(csv_file, edge.drug.cid, "DRUG", "HAS_SUBSTRUCTURE", "SUBSTRUCTURE",
                           edge.feature.id, "1", "")
            count += 1
            # print(f"{count} / {total} substructures done")

    def select_entries(self, limit):
        drugs = []
        indications = []
        adrs =[]
        structs = []
        targets = []

        for drug in random.choices(Drug.objects.all(), k=limit):
            drugs.append(drug)
            for edge in Edge.objects.filter(drug=drug):
                if edge.edge_type == "DRUG_TARGET":
                    targets.append(edge)
                elif edge.edge_type == "INDICATED_FOR":
                    indications.append(edge)
                elif edge.edge_type == "HAS_SUBSTRUCTURE":
                    structs.append(edge)
                elif edge.edge_type == "HAS_SIDE_EFFECT":
                    adrs.append(edge)
        print("Inds: ", len(indications))
        print("Adrs: ", len(adrs))
        print("Structs: ", len(structs))
        print("Targets: ", len(targets))
        return drugs, indications, adrs, structs, targets
