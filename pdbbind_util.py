import csv


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


def get_id_mapping(filename):   # call with "./data/drugTable.csv"
    with open(filename, 'r') as f:
        lines = csv.reader(f, delimiter=",")
        id_map = {}
        for index, line in enumerate(lines):
            if not index:
                continue
            if not line:
                continue
            drugbank_id, ligand_id = line[2], line[4]
            id_map[drugbank_id] = ligand_id
        return id_map


def get_pdbbind_ligands(filename):  # "./data/PDBBind/index/INDEX_refined_data.2018"
    with open(filename,'r') as f:
        lines = f.readlines()
    all_ligands = set()
    for index, line in enumerate(lines):
        if index < 6 or not line:
            continue
        code = line.split()[7]
        all_ligands.add(code[1:-1])
    return all_ligands

