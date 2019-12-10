import os
import sys

# if __name__ == "__main__":
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
from .sider_utils import *
from adr.models import *
from .pdbbind_utils import *
from .substructure_utils import get_fingerprint


class Command(BaseCommand):
    help = "Populate the database with ADR-drug and indication-drug edges"

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix_units',
            action='store_true',
            help='Convert all binding values to nM'
        )

    def handle(self, *args, **options):
        total = len(Edge.objects.filter(edge_type="DRUG_TARGET"))
        count = 0
        for edge in Edge.objects.filter(edge_type="DRUG_TARGET"):
            if edge.weight_units == "mM":
                edge.weight_units = "nM"
                edge.weight_value *= 1000000
            if edge.weight_units == "uM":
                edge.weight_units = "nM"
                edge.weight_value *= 1000
            if edge.weight_units == "pM":
                edge.weight_units = "nM"
                edge.weight_value /= 1000
            count += 1
            print(f"{count} / {total} done")
