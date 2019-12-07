import csv

STRUCT_LINKS = "./adr/management/commands/data/sider/structure_links.csv"
INDICATION = "./adr/management/commands/data/sider/meddra_all_indications.tsv"
ADRS = "./adr/management/commands/data/sider/meddra_all_se.tsv"
ATCs = "./adr/management/commands/data/sider/drug_atc.tsv"
IDS = "./adr/management/commands/data/drugTable.csv"


def process_csv(filename, delimiter, process_func):
    with open(filename, 'r') as map:
        lines = csv.reader(map, delimiter=delimiter)
        for index, line in enumerate(lines):
            process_func(index, line)


def cid_to_atc():
    cid_atc = {}

    def process_func(index, line):
        if index and len(line) >= 2:
            cid_atc[line[0]] = line[1]  # maps CID of drug to ATC of drug

    process_csv(ATCs, "\t", process_func)
    return cid_atc


def atc_to_ligandId():
    atc_ligand = {}

    def process_func(index, line):
        if index and len(line) >= 5 and line[3] and line[4]:
            for atc in line[3].split("#"):
                atc_ligand[atc] = line[4]  # maps ATC of drug to 3-letter ligand id

    process_csv(IDS, ",", process_func)
    return atc_ligand


def cid_to_ligandId():
    cid_atc = cid_to_atc()
    atc_ligand = atc_to_ligandId()
    return {cid: atc_ligand[cid_atc[cid]] for cid in cid_atc if cid_atc[cid] in atc_ligand}


def cid_to_drugbank():
    cid_to_db = {}

    def process_func(index, line):
        if index and line[10] and line[0]:
            cid_to_db["CID" + line[10]] = (line[0], line[3])  # maps to tuple of drugbankid, group of drugs
    process_csv(STRUCT_LINKS, ",", process_func)
    return cid_to_db


def cid_to_smiles():
    cid_to_smiles = {}

    def process_func(index, line):
        if index and line[10] and line[6]:
            cid_to_smiles["CID" + line[10]] = line[6]  # maps to tuple of drugbankid, group of drugs

    process_csv(STRUCT_LINKS, ",", process_func)
    return cid_to_smiles


def cid_to_indication():
    cid_to_ind = {}

    def process_func(index, line):
        if index:
            cid_to_ind.setdefault(line[0], set()).add(line[5])

    process_csv(INDICATION, "\t", process_func)
    return cid_to_ind


def cid_to_adr():
    cid_adr = {}

    def process_func(index, line):
        if index and len(line) >= 5 and line[0] and line[4]:
            cid_adr.setdefault(line[0], set()).add(line[4])

    process_csv(ADRS, "\t", process_func)
    return cid_adr


if __name__ == "__main__":
    # print(cid_to_atc())
    # print(atc_to_ligandId())
    # print(cid_to_ligandId())
    # print(cid_to_indication())
    # print(cid_to_adr())
    pass

