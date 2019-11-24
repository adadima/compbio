import adr.models as m


def add_edge(drugbank_id, drug_smiles, edge_type, feature_id, edge_weight,  edge_units):
    drug = m.Drug(drugbank_id=drugbank_id, smiles=drug_smiles)
    drug.save()
    edge = m.Edge(edge_type=edge_type, drug=drug, edge_weight=edge_weight, edge_units=edge_units)

    if edge_type == "HAS_SUBSTRUCTURE":
        substructure = m.SubStructure()
        pass
    if edge_type == "HAS_SIDE_EFFECT":
        pass
    if edge_type == "INDICATED_FOR":
        pass
    if edge_type == "DRUG_TARGETS":
        pass
