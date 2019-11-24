import csv
from pdbbind_util import *

ID_MAP = "./data/drugTable.csv"
INDEX_NAME = "./data/PDBBind/index/INDEX_refined_name.2018"
INDEX_DATA = "./data/PDBBind/index/INDEX_refined_data.2018"


def get_binding_affinity():
    with open(INDEX_DATA, 'r') as f:
        lines = f.readlines()
    affinity = {}  # maps tuples of (pdb, ligand_code) to tuples of (aff_value, aff_unit, aff_measure)
    for index, line in enumerate(lines):
        if index < 6 or not line:
            continue
        pdb, resolution, year, logK, k, ref1, ref2, ligand = line.split()
        aff_measure = k.split("=")[0]
        aff_value = k.split("=")[1][:-2]
        aff_units = k.split("=")[1][-2:]
        affinity[pdb, ligand[1:-1]] = [aff_value, aff_units, aff_measure]

    return affinity


def get_binding_info(filename):
    new_lines = []
    drugbank_to_code = get_id_mapping(ID_MAP)
    pdb_to_uniprot = get_pdb_uniprot_map(INDEX_NAME)
    aff = get_binding_affinity()
    affinity = {(pdb_to_uniprot[pdb], ligand): aff[pdb,  ligand] for (pdb, ligand) in aff}
    count = 0
    total = 0
    with open(filename, 'r') as f:
        lines = csv.reader(f, delimiter=",")
        for index, line in enumerate(lines):
            if not index:
                new_lines.append(line + ["weight", "units", "measure"])
                continue

            if line[2] == "DRUG_TARGETS":
                total += 1
                ligand, uniprot = line[0], line[1]
                if ligand in drugbank_to_code and (uniprot, drugbank_to_code[ligand]) in affinity:
                    extra_columns = affinity[uniprot, drugbank_to_code[ligand]]
                    new_lines.append(line + extra_columns)
                    count += 1
                else:
                    new_lines.append(line)
                print(new_lines[-1])
            else:
                new_lines.append(line + ["1", "-", "-"])
    print(count/total)
    return new_lines


if __name__ == "__main__":
    get_binding_info("./data/example_graph.csv")
