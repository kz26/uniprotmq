from django import forms
from django.conf import settings

OUTPUT_FIELDS = (
    ('uniprot_name', 'UniProt name'),
    ('uniprot_acc', 'UniProt accession'),
    ('RefSeq', 'RefSeq'),
    ('Ensembl', 'Ensembl'),
    ('IPI', 'IPI ID'),
    ('GeneID', 'GeneID'),
    ('gene_name', 'Gene name'),
    ('GI', 'GI accession'),
    ('description', 'description')
)

OUTPUT_FIELDS_DICT = dict(OUTPUT_FIELDS)
DATABASES = [(x, x) for x in settings.MYDB_NAMES]

class QueryForm(forms.Form):
    database = forms.ChoiceField(choices=DATABASES)
    input_data = forms.CharField(widget=forms.Textarea, required=False)
    input_file = forms.FileField(label="or, upload an input file", required=False)
    outputs = forms.MultipleChoiceField(choices=OUTPUT_FIELDS, widget=forms.SelectMultiple(attrs={'size': len(OUTPUT_FIELDS)}))

    def clean(self):
        cleaned_data = super(QueryForm, self).clean()
        input_data = cleaned_data.get('input_data')
        input_file = cleaned_data.get('input_file')
        if not (input_data or input_file): 
            raise forms.ValidationError("Please enter input data or upload an input file.")
    
        return cleaned_data
