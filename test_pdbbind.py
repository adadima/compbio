import csv


def get_id_mapping(filename):
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


def get_pdbbind_ligands(filename):
    with open(filename,'r') as f:
        lines = f.readlines()
    all_ligands = set()
    for index, line in enumerate(lines):
        if index < 6 or not line:
            continue
        code = line.split()[7]
        all_ligands.add(code[1:-1])
    return all_ligands


def count_overlap(graph_file, id_mapping_file, pdb_file):
    id_map = get_id_mapping(id_mapping_file)
    ligands = get_pdbbind_ligands(pdb_file)

    drug_bank_drugs = set()
    with open(graph_file, 'r') as f:
        lines = csv.reader(f, delimiter=",")
        for line in lines:
            if line:
                drug_bank_drugs.add(line[0])
    total = len(drug_bank_drugs)
    return sum(id_map[drug] in ligands for drug in drug_bank_drugs if drug in id_map) / total


if __name__ == "__main__":
    print(count_overlap("./data/example_graph.csv",
                        "./data/drugTable.csv",
                        "./data/PDBBind/index/INDEX_general_PL_data.2018"))
