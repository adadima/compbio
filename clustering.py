import sys


class Pocket:
    def __init__(self, pdb: str, sequnece: str):
        self.pdb = pdb
        self.seq = sequnece

    def get_distance(self, other):
        if not isinstance(other, Pocket):
            raise Exception(f"Can only compare object of type Protein, not {type(other)}")
        return 0


class Cluster:
    ID = 0

    def __init__(self, items: set):
        self.items = items
        self.id = self.ID
        self.ID += 1

    def merge(self, other):
        if not isinstance(other, Cluster):
            raise Exception(f"Can only merge object of type Cluster with {type(other)}")
        items = set()
        [items.add(item) for item in self.get_items()]
        [items.add(item) for item in other.get_items()]
        return Cluster(items)

    def add_item(self, item):
        self.items.add(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items

    def get_distance(self, other):
        if not isinstance(other, Cluster):
            raise Exception(f"Can only merge object of type Cluster with {type(other)}")
        sum(item1.get_distance(item2) for item1 in self.get_items() for item2 in other.get_items())


num_clusters = sys.argv[1]


def cluster(pocket_generator):
    pockets = pocket_generator()
    total_pockets = len(pockets)

    for num in range(total_pockets, num_clusters - 1, -1):
        cluster1, cluster2 = closest_pair(pockets)
        pockets = [c for c in pockets if c != cluster1 and c != cluster2]
        pockets.append(cluster1.merge(cluster2))

    return pockets


def closest_pair(clusters):
    closest = None
    distance = None

    for p1 in clusters:
        for p2 in clusters:

            if p1 == p2:
                continue

            current_distance = p1.get_distance(p2)
            if closest is None or current_distance < distance:
                closest = (p1, p2)
                distance = current_distance

    return closest
