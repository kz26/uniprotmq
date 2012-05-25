#!/usr/bin/python
# Reads an ID mapping file
# prints out the GIs only

import sys
import re

UNIPROT_NAME_PAT = re.compile("^[A-Z0-9]+_([A-Z]+)$")

with open(sys.argv[1], 'r') as f:
    species = sys.argv[2:]
    current = ''
    for line in f:
        l = line.rstrip().split('\t')
        if l[1] == 'UniProtKB-ID':
            current = l[2]
        elif l[1] == 'GI':
            m = UNIPROT_NAME_PAT.search(current)
            if (m and m.group(1) in species) or not species:
                o = [current, 'GI', l[2], '0']
                print "\t".join(o)
