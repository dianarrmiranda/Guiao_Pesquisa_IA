from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

mapa_a = {
    "A": "BED",
    "B": "AEC",
    "C": "BED",
    "D": "AEC",
    "E": "ABCD"
}

mapa_b = {
    "A": "BED",
    "B": "AEC",
    "C": "BEF",
    "D": "AEF",
    "E": "ABCDF",
    "F": "DEC"
}

mapa_c = {
    "A": "DEFB",
    "B": "AFC",
    "C": "BFGD",
    "D": "AEGC",
    "E": "AFGD",
    "F": "ABCGE",
    "G": "DEFC"
}

def make_constraint_graph(mapa):
    return { (X,Y): lambda r1, c1, r2, c2: c1 != c2 for X in mapa.keys() for Y in mapa[X] }

def make_domains(regions, colors):
    return {region: colors for region in regions}

cs = ConstraintSearch(make_domains(mapa_a.keys(), colors), make_constraint_graph(mapa_a))
print(cs.search())

csb = ConstraintSearch(make_domains(mapa_b.keys(), colors), make_constraint_graph(mapa_b))
print(csb.search())

csc = ConstraintSearch(make_domains(mapa_c.keys(), colors), make_constraint_graph(mapa_c))
print(csc.search())


