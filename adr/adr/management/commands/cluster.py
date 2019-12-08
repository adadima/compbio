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
from clustering import *


class Command(BaseCommand):
    help = "Analyze the adr database."
    cluster_to_target = {}
    target_to_cluster = {}

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Replace the Target entries in the database with the computed clusters'
        )

    def handle(self, *args, **options):
        self.cluster()
        if options['replace']:
            self.add_pockets()

    def cluster(self):
        print("Computing clusters ... ")
        pockets = []
        for target in Target.objects.all():
            c = Cluster({Pocket(target.pdb[0], target.protein_pocket_sequence)})
            pockets.append(c)
            self.cluster_to_target.setdefault(c.id, set()).add(target)
            self.target_to_cluster[target] = c.id

        clusters = cluster(lambda: pockets)
        id = 0
        for c in clusters:
            pdbs = "".join(pocket.pdb for pocket in c.get_items())
            print(f"Cluster {id}: {pdbs}")
            id += 1

    def add_pockets(self):
        for edge in Edge.objects.all():

            if edge.edge_type != "DRUG_TARGET":
                continue
            cluster_id = self.target_to_cluster[edge.feature]
            motif = PocketMotif(motif_id=cluster_id, proteins=self.cluster_to_target[cluster_id])
            motif.save()
            edge.feature = motif
            edge.edge_type = "DRUG_MOTIF"
            edge.save()