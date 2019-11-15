from openbabel import pybel
import csv


def get_fingerprint(smiles_string):
    molecule = pybel.readstring("smi", smiles_string)
    fingerprint = molecule.calcfp()
    return fingerprint.fp, fingerprint.bits


def add_edges(graph_file, db_to_smiles):
    drugbank_ids = generate_drug_ids(graph_file)
    with open(graph_file, 'r') as f:
        lines = f.readlines()
    with open(graph_file, 'w') as f:
        [f.write(line) for line in lines]
        for drug_id in drugbank_ids:
            if drug_id not in db_to_smiles:
                continue
            smiles_string = db_to_smiles[drug_id]
            for substructure_id in get_fingerprint(smiles_string)[1]:
                f.write(f"{drug_id},{substructure_id},HAS_SUBSTRUCTURE\n")


def drugbank_to_smiles(filename):
    id_mapping = {}
    with open(filename, 'r') as f:
        lines = csv.reader(f, delimiter=",")
        for index, line in enumerate(lines):
            if not index:
                continue

            db_id, name, cas, group, inchi_key, inchi, smiles, \
            formula, kegg1, kegg2, pubchem1, pubchem2, chebl, \
            chembl, het, chem_spider, bindingDB = line

            if db_id and smiles:
                id_mapping[db_id] = smiles

    return id_mapping


def generate_drug_ids(graph_file):
    with open(graph_file, 'r') as f:
        lines = csv.reader(f, delimiter=",")
        return {line[0] for line in lines if line[0] and line[0] != "DrugBank"}


def add_substructures(graph_file, ids_file):
    add_edges(graph_file, drugbank_to_smiles(ids_file))


if __name__ == "__main__":
    fp, bits = get_fingerprint("CC(=O)C(O)=O")
    print([item  for item in fp])
    # add_substructures("./data/example_graph.csv", "./data/structure_links.csv")
