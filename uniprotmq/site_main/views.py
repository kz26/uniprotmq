# Create your views here.
from django.http import *
from django import forms
from django.shortcuts import *
from uniprotmq.site_main.models import *
from uniprotmq.site_main.forms import *
from uniprotmq.site_main import idparser
from cStringIO import StringIO

def search(request):
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            response = HttpResponse(mimetype='text/plain')
            col_headers = ['Input']
            col_headers.extend([OUTPUT_FIELDS_DICT[x] for x in form.cleaned_data['outputs']])
            response.write("\t".join(col_headers) + '\n')

            dbi = UniProtInterface(form.cleaned_data['database'])

            if form.cleaned_data.get('input_data'):
                indata = form.cleaned_data.get('input_data').split('\n')
            else:
                fs = request.FILES['input_file'].read()
                indata = StringIO(fs)


            for line in indata:
                l = line.strip().upper()
                if not l:
                    continue

                up_names = []

                results = {}
                for f in form.cleaned_data['outputs']:
                    results[f] = []
                line = [l]

                try:
                    idt = idparser.get_id_type(l)
                    if idt == 'uniprot_name':
                        up_names.append(l)
                    else:
                        for n in dbi.session.query(IDMapping.id).filter(IDMapping.resource == idt).filter(IDMapping.value == l):
                            up_names.append(n.id)
                    
                    if up_names:
                        q_idm = dbi.session.query(IDMapping).filter(IDMapping.id.in_(up_names))
                        for x in q_idm:
                            if x.resource in results:
                                results[x.resource].append(x.value)

                        if 'description' in results:
                            q_e = dbi.session.query(Entry).filter(Entry.id.in_(up_names))
                            for x in q_e:
                                if x.description:
                                    results['description'].append(x.description)

                        if idt == 'uniprot_acc' and len(up_names) > 1:
                            line[0] = "%s (DEMERGED)" % (l)
                        else:
                            for f in form.cleaned_data['outputs']:
                                line.append("|".join(set(results[f])))
                except:
                    pass 
                response.write("\t".join(line) + "\n")
            return response

    else:
        form = QueryForm()
    return render(request, 'search.html', dictionary={'form': form})

