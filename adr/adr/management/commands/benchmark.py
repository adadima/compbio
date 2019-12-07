import os
import sys


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
    help = "Analyze the adr database."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        complete = Edge.objects.filter(drug__isnull=False,
                                       feature__isnull=False,
                                       edge_type__isnull=False,
                                       weight_value__isnull=False).count()
        total = Edge.objects.all().count()
        targets = Target.objects.filter(protein_pocket_sequence__isnull=False).count()
        total_targets = Target.objects.all().count()

        print(f"Complete edges {complete} / {total}")
        print(f"Complete proteins: {targets} / {total_targets}")
        print(f"All Drugs: {Drug.objects.all().count()}")
        print(f"All SubStructures: {SubStructure.objects.all().count()}")
        print(f"All ADRs: {ADR.objects.all().count()}")
        print(f"All Indications: {Indication.objects.all().count()}")


