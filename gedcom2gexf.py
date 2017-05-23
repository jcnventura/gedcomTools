#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Works with Python2 and Python3

import gedcom
import itertools
import networkx as nx
import os

def gedcom2gephi(gedcomFilename = 'gedcom.ged', gephiFilename = None):
    getId = lambda n: n.id[1:-1]
    getFirstName = lambda n: '' if n.name[0] is None else n.name[0]
    getFamilyName = lambda n: '' if n.name[1] is None else n.name[1]
    getName = lambda n: getFirstName(n)+' '+getFamilyName(n)
    getValue = lambda n: n.value[1:-1]

    g = gedcom.parse(gedcomFilename)
    dg = nx.Graph()
    for p in g.individuals:
        if p.id not in dg:
            dg.add_node(getId(p), label=getName(p)+' ('+getId(p)+')', name=getName(p), familyName=getFamilyName(p))
    for p in g.individuals:
        if p.father:
            dg.add_edge(getId(p.father), getId(p), label='Father')
        if p.mother:
            dg.add_edge(getId(p.mother), getId(p), label='Mother')
    for f in g.families:
        for s in itertools.combinations(f.partners, 2):
            dg.add_edge(getValue(s[0]), getValue(s[1]), label='Spouse')
    if gephiFilename is None:
        gephiFilename = os.path.splitext(gedcomFilename)[0] + '.gexf'
    nx.write_gexf(dg, gephiFilename)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description = 'This script converts a gedcom file to a gexf file')
    parser.add_argument('-g','--gedcom', type = str, default = 'my_gedcom_file.ged',
                       help = 'Gedcom filename')
    parser.add_argument('-o','--outputGexf', type = str, default = None,
                       help='Optional output name. If not provided, a filename will be generated from the gedcom filename')
    args = parser.parse_args()
    gedcom2gephi(gedcomFilename = args.gedcom, gephiFilename = args.outputGexf)
