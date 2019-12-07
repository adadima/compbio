from openbabel import pybel


def get_fingerprint(smiles_string):
    molecule = pybel.readstring("smi", smiles_string)
    fingerprint = molecule.calcfp()
    return fingerprint.fp, fingerprint.bits

