#!/usr/bin/python
# reads a DAT file and prints out it in a db-friendly format

import datparser

import sys

# a handy line-printing class
class LinePrinter:
    def __init__(self, n):
        self.n = n

    def println(self, o, res, val, is_primary=0):
        o.write("%s\t%s\t%s\t%s\n" % (self.n, res, val, is_primary))

    def println_simple(self, o, val):
        o.write("%s\t%s\n" % (self.n, val))

    def printlist_fp(self, o, res, val): # takes a list, prints first as primary
        self.println(o, res, val[0], 1)
        for x in val[1:]:
            self.println(o, res, x)

out = open(sys.argv[2], 'w')
out_desc = open(sys.argv[3], 'w')

for p in datparser.read_dat(sys.argv[1]):
    printer = LinePrinter(p['ID'][0])
    # the ID line / entry name
    printer.println(out, 'uniprot_name', printer.n, 1)

    # accession numbers
    printer.printlist_fp(out, 'uniprot_acc', p['AC'])

    # description
    printer.println_simple(out_desc, p['DE'][0])
    
    # gene names
    if 'GN' in p:
        printer.printlist_fp(out, 'gene_name', p['GN'])
    
    # cross-refs
    if 'DR' in p:
        for x in p['DR']:
            res = x[0]
            if res == 'Ensembl':
                printer.println(out, res, x[2])
            elif res in ['GeneID', 'IPI', 'RefSeq']:
                printer.println(out, res, x[1])
