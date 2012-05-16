#!/usr/bin/python
# Reads an ID mapping file
# prints out the GIs only

import sys

with open(sys.argv[1], 'r') as f:
    current = ''
    for line in f:
        l = line.rstrip().split('\t')
        if l[1] == 'UniProtKB-ID':
            current = l[2]
        elif l[1] == 'GI':
            o = [current, 'GI', l[2], '0']
            print "\t".join(o)
