import os

from dateutil.parser import parse as date_parse

from webrequests import WebRequest as WR
from simple_loggers import SimpleLogger


class OMIM(object):
    def __init__(self, omim_url='https://mirror.omim.org'):
        self.omim_url = omim_url
        self.logger = SimpleLogger('OMIM')

    def get_soup(self, url):
        soup = WR.get_soup(url)
        return soup

    def get_mim2gene(self, outfile=None):
        url = self.omim_url + '/static/omim/data/mim2gene.txt'
        resp = WR.get_response(url, stream=True)
        if outfile:
            with open(outfile, 'wb') as out:
                for chunk in resp.iter_content(chunk_size=512):
                    out.write(chunk)
            self.logger.debug(f'save file: {outfile}')
        else:
            return resp.text

    def parse_mim2gene(self, mim2gene=None, mim_types=('gene', 'gene/phenotype')):
        if mim2gene and os.path.isfile(mim2gene):
            self.logger.debug(f'parsing mim2gene from file: {mim2gene} ...')
            text = open(mim2gene).read().strip()
        else:
            self.logger.debug(f'parsing mim2gene from website ...')
            text = self.get_mim2gene()

        fields = 'mim_number mim_type entrez_gene_id hgnc_gene_symbol ensembl_gene_id'.split()
        for line in text.split('\n'):
            if line.startswith('# Generated:'):
                generated = line.split(': ')[-1]
                continue
            elif line.startswith('#') or not line.strip():
                continue
            linelist = line.split('\t')
            context = dict(zip(fields, linelist))

            if mim_types and context['mim_type'] not in mim_types:
                continue

            context['generated'] = date_parse(generated)
            yield context['mim_number'], context


if __name__ == '__main__':
    omim = OMIM()

    # resp = omim.get_mim2gene()
    # print(resp.text[:500])
    
    # omim.get_mim2gene('mim2gene.txt')

    # omim.parse_mim2gene('mim2gene.txt')
    # contexts = omim.parse_mim2gene('mim2gene.txt', mim_types=('gene/phenotype',))
    contexts = omim.parse_mim2gene('mim2gene.txt', mim_types=None)
    for context in contexts:
        print(context)
