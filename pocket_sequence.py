import csv
from Bio.PDB.PDBParser import PDBParser
from Bio.SeqIO.PdbIO import AtomIterator


def get_uniprot_pdb_map(index_filename):  # use ./data/PDBBind/index/INDEX_general_PL_name.2018
    with open(index_filename, 'r') as f:
        lines = f.readlines()
    map = {}
    for index, line in enumerate(lines):
        if index < 6 or not line:
            continue
        tokens = line.split()
        map.setdefault(tokens[2], set()).add(tokens[0])
    return map


def get_sequences_from_pdb(pdb_id, set_name):
    parser = PDBParser(PERMISSIVE=1)
    structure = parser.get_structure(pdb_id, f"./data/{set_name}/{pdb_id}/{pdb_id}_pocket.pdb")
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


def add_sequence(graph_filename, output_filename, index_PL_name, set_name):
    sequences = get_all_sequences(graph_filename, index_PL_name, set_name)

    with open(output_filename, 'w') as f:
        for uniprot in sequences:
            seqs = "    ".join(sequences[uniprot])
            f.write(f"{uniprot} {seqs}\n")


if __name__ == "__main__":
    # print(get_uniprot_pdb_map("./data/PDBBind/index/INDEX_refined_name.2018"))
    # print(get_sequences_from_pdb("1a1e", "refined-set"))
    # print(get_all_sequences("./data/example_graph.csv",
    #              "./data/PDBBind/index/INDEX_refined_name.2018",
    #              "refined-set"))
    add_sequence("./data/example_graph.csv",
                 "./data/out/target_sequences.txt",
                 "./data/PDBBind/index/INDEX_refined_name.2018",
                 "refined-set")
