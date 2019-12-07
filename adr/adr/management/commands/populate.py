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

    def add_indication(self):
        cid_to_ind = cid_to_indication()
        total = sum(len(cid_to_ind[c]) for c in cid_to_ind)
        count = 0
        for cid in cid_to_ind:
            drug, _ = Drug.objects.get_or_create(cid=cid)
            drug.save()
            for ind in cid_to_ind[cid]:
                indication, _ = Indication.objects.get_or_create(indication_id=ind)
                indication.save()
                edge, _ = Edge.objects.get_or_create(edge_type="INDICATED_FOR", drug=drug, feature=indication,
                            weight_value=1)
                edge.save()
                count += 1
                print(f"{count}/{total} done")

    def add_adr(self):
        cid_to_adrs = cid_to_adr()
        total = sum(len(cid_to_adrs[c]) for c in cid_to_adrs)
        count = 0
        for cid in cid_to_adrs:
            drug, _ = Drug.objects.get_or_create(cid=cid)
            drug.save()
            for adr_ in cid_to_adrs[cid]:
                adr, _ = ADR.objects.get_or_create(adr_id=adr_)
                adr.save()
                edge, _ = Edge.objects.get_or_create(edge_type="HAS_SIDE_EFFECT", drug=drug, feature=adr,
                            weight_value=1)
                edge.save()
                count += 1
                print(f"{count}/{total} done")

    def add_targets(self, name_file, data_file, set='refined-set'):
        cid_to_ligand = cid_to_ligandId()
        ligand_to_cid = {cid_to_ligand[ligand]: ligand for ligand in cid_to_ligand}
        pdb_to_uniprot = get_pdb_uniprot_map(name_file)
        affinities = get_binding_affinity(data_file)
        # print(ligand_to_cid.keys())
        # print({key[1] for key in affinities})
        total = len(affinities)
        count = 0
        for key in affinities:
            pdb, ligandId = key
            if ligandId not in ligand_to_cid:
                # print("FAIL LIGAND")
                continue
            if pdb not in pdb_to_uniprot:
                # print("FAIL PDB")
                continue
            self.add_drug_target(ligandId, pdb, affinities, ligand_to_cid, pdb_to_uniprot, set)
            count += 1
            print(f"{count} / {total} done")

    def add_drug_target(self, ligandId, pdb, affinities, ligand_to_cid, pdb_to_uniprot, set):
        aff_value, aff_units, aff_measure = affinities[pdb, ligandId]
        drug, _ = Drug.objects.get_or_create(cid=ligand_to_cid[ligandId])
        target, _ = Target.objects.get_or_create(uniprot=pdb_to_uniprot[pdb])
        try:
            target.protein_pocket_sequence = "\n".join(get_sequences_from_pdb(pdb, set_name=set))
        except:
            pass

        edge, _ = Edge.objects.get_or_create(edge_type="DRUG_TARGET", drug=drug,
                                             feature=target, weight_value=aff_value,
                                             weight_units=aff_units, weight_measure=aff_measure)
        drug.save()
        target.save()
        edge.save()

    def add_substructure(self):
        cid_to_str = cid_to_smiles()
        total = len(cid_to_str)
        count = 0
        for cid, smiles in cid_to_str.items():
            drug, _ = Drug.objects.get_or_create(cid=cid)
            drug.save()
            for substructure_id in get_fingerprint(smiles)[1]:
                # print("Subs id: ", substructure_id)
                substructure, _ = SubStructure.objects.get_or_create(struct_id=substructure_id)
                edge, _ = Edge.objects.get_or_create(edge_type="HAS_SUBSTRUCTURE", drug=drug,
                                                     feature=substructure, weight_value=1)

                substructure.save()
                edge.save()
            count += 1
            print(f"{count} / {total} done")

    def add_arguments(self, parser):
        parser.add_argument(
            '--targets',
            action='store_true',
            help='Populate the database with drug-target edges'
        )

        parser.add_argument(
            '--refined',
            action='store_true',
            help="Use the refined pdb set."
        )

        parser.add_argument(
            '--general',
            action='store_true',
            help="Use the general pdb set."
        )

        parser.add_argument(
            '--adrs',
            action='store_true',
            help='Populate the database with drug-adr edges'
        )

        parser.add_argument(
            '--inds',
            action='store_true',
            help='Populate the database with drug-indication edges'
        )

        parser.add_argument(
            '--substruct',
            action='store_true',
            help='Populate the database with drug-substructure edges'
        )

        parser.add_argument(
            '--test',
            action='store_true',
            help='Runs a test.'
        )

    def handle(self, *args, **options):
        if options['targets']:
            if options['refined']:
                self.add_targets(INDEX_NAME_REFINED, INDEX_DATA_REFINED)
            elif options['general']:
                self.add_targets(INDEX_NAME_GENERAL, INDEX_DATA_GENERAL, 'general-set')
            else:
                print("If you are trying to add targets you need to specify"
                      "what PDBBind set to use - general or refined.")
            print(Drug.objects.all().count())
            print(Target.objects.all().count())
        if options['adrs']:
            self.add_adr()
            print(Drug.objects.all().count())
            print(ADR.objects.all().count())
        if options['inds']:
            self.add_indication()
            print(Drug.objects.all().count())
            print(Indication.objects.all().count())
        if options['substruct']:
            self.add_substructure()
            print(Drug.objects.all().count())
            print(SubStructure.objects.all().count())
        if options['test']:
            print("Arguments working")
        print("Executed command")
        print(os.getcwd())


if __name__ == "__main__":
    pass
