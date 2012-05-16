#!/usr/bin/python
# very simple dat parsing library
# currently only parses ID, AC, DE, GN, and DR lines

import re

LINE_PATTERNS = {
    'de-full': re.compile(r'^DE {3}RecName: Full=(.*);$'),
    'de-sub': re.compile(r'^DE {3}SubName: Full=(.*);$'),
    'gene-name': re.compile(r'Name=(.*?);')
}   

def parse_line(l):
    h = l[:2]
    lc = l[5:].rstrip()
    v = None
    if h == 'ID':
        v = [re.split(' +', lc)[0]]
    elif h == 'AC':
        temp = lc.rstrip(';').split(';')
        v = [x.strip() for x in temp]
    elif h == 'DE':
        m = LINE_PATTERNS['de-full'].search(l)
        if m:
            v = [m.group(1)]
        else:
            m = LINE_PATTERNS['de-sub'].search(l)
            if m:
                v = [m.group(1)]
    elif h == 'GN':
        m = LINE_PATTERNS['gene-name'].search(l)
        if m:
            v = [m.group(1)]
    elif h == 'DR':
        v = [[x.strip() for x in re.split('; ?', lc.rstrip('.'))]]
    if v:
        return (h, v)
    return None
        
def read_dat(fn):
    with open(fn, 'r') as f:
        prot = {}
        for line in f:
            if line[:2] == '//':
                result = prot.copy()
                prot = {}
                yield result
            pl = parse_line(line)
            if pl:
                h = pl[0]
                if h not in prot:
                    prot[h] = []
                prot[h].extend(pl[1])

