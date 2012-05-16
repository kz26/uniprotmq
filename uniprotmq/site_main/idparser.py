import re
from exceptions import ValueError

PATTERNS = (
    ('IPI', re.compile(r"IPI")),
    ('RefSeq', re.compile(r"NP_")),
    ('GI', re.compile(r"GI:")),
    ('GeneID', re.compile(r"[0-9]+")),
    ('Ensembl', re.compile(r"ENS[A-Z]*?[0-9]+$")),
    ('uniprot_name', re.compile(r"[A-Z0-9]+_[A-Z]+$")),
    ('uniprot_acc', re.compile(r"[A-NR-Z]\d[A-Z][A-Z\d]{2}\d(?:-[A-Z0-9]+)?$")),
    ('uniprot_acc', re.compile(r"[OPQ]\d[A-Z\d]{3}\d(?:-[A-Z0-9]+)?$")),
    ('gene_name', re.compile(r"[A-Z0-9]+"))
)

def get_id_type(i):
    for p in PATTERNS:
        if p[1].match(i):
            return p[0]
    raise ValueError("Unrecognized input type")
