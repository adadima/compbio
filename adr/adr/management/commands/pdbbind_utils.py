import csv
from Bio.PDB.PDBParser import PDBParser
from Bio.SeqIO.PdbIO import AtomIterator


def extract_from_file(filename, function):
    with open(filename) as f:
        lines = f.readlines()
    map = {}
    for index, line in enumerate(lines):
        function(map, index, line)
    return map


def get_ligand_to_pdb(data_filename):

    def extract_info(map, index, line):
        if index >= 6 and line:
            tokens = line.split()
            map.setdefault(tokens[7][1:-1], set()).add(tokens[1])

    return extract_from_file(data_filename, extract_info)


def get_uniprot_pdb_map(index_filename):  # use ./data/PDBBind/index/INDEX_refined_name.2018
    with open(index_filename, 'r') as f:
        lines = f.readlines()
    map = {}
    for index, line in enumerate(lines):
        if index < 6 or not line:
            continue
        tokens = line.split()
        map.setdefault(tokens[2], set()).add(tokens[0])
    return map


def get_pdb_uniprot_map(index_filename):
    uniprot_pdb = get_uniprot_pdb_map(index_filename)
    revert = {}
    for uniprot in uniprot_pdb:
        for pdb in uniprot_pdb[uniprot]:
            revert[pdb] = uniprot
    return revert

POCKET_BASE_PATH = "./adr/management/commands/data/"


def get_sequences_from_pdb(pdb_id, set_name="refined-set"):
    parser = PDBParser(PERMISSIVE=1)
    structure = parser.get_structure(pdb_id, f"{POCKET_BASE_PATH}{set_name}/{pdb_id}/{pdb_id}_pocket.pdb")
    return [record.seq._data for record in AtomIterator(pdb_id, structure)]


def get_sequneces_from_uniprot(uniprot,  uniprot_to_pdb, set_name):
    if uniprot not in uniprot_to_pdb:
        return []
    seqs = []
    for pdb in uniprot_to_pdb[uniprot]:
        seqs.extend(get_sequences_from_pdb(pdb, set_name))
    return seqs


def get_all_sequences(graph_filename, index_PL_name, set_name):
    uniprot_to_pdb = get_uniprot_pdb_map(index_PL_name)
    sequences = {}
    with open(graph_filename, 'r') as f:
        lines = csv.reader(f, delimiter=",")
        for index, line in enumerate(lines):
            if line[2] == "DRUG_TARGETS" and line[1] not in sequences:
                sequences[line[1]] = get_sequneces_from_uniprot(line[1], uniprot_to_pdb, set_name)
    return sequences

import csv

# ID_MAP = "./data/drugTable.csv"
INDEX_NAME_REFINED = "./adr/management/commands/data/PDBBind/index/INDEX_refined_name.2018"
INDEX_DATA_REFINED = "./adr/management/commands/data/PDBBind/index/INDEX_refined_data.2018"

INDEX_NAME_GENERAL = "./adr/management/commands/data/PDBBind/index/INDEX_general_PL_name.2018"
INDEX_DATA_GENERAL = "./adr/management/commands/data/PDBBind/index/INDEX_general_PL_data.2018"


def get_binding_affinity(index_file):
    with open(index_file, 'r') as f:
        lines = f.readlines()
    affinity = {}  # maps tuples of (pdb, ligand_code) to tuples of (aff_value, aff_unit, aff_measure)
    for index, line in enumerate(lines):
        if index < 6 or not line:
            continue
        # print(line)
        line = line.replace(' )', ')')
        # print(line)
        pdb, resolution, year, logK, k, ref1, ref2, ligand = line.split()[:8]
        k = k.replace('~', '=').replace('>', '=').replace('<', '=')
        aff_measure = k.split("=")[0]
        aff_value = k.split("=")[1][:-2]
        aff_units = k.split("=")[1][-2:]
        affinity[pdb, ligand[1:-1]] = [aff_value, aff_units, aff_measure]

    return affinity
