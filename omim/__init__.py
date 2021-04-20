import os
import json


HOME = os.path.expanduser('~')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'version', 'version.json')))

__version__ = version_info['version']

DEFAULT_DB = os.path.join(BASE_DIR, 'data', 'omim.sqlite3')

if not os.path.isfile(DEFAULT_DB):
    DEFAULT_DB = os.path.join(HOME, 'omim_data', 'omim.sqlite3')

DEFAULT_URL = 'https://mirror.omim.org'

MIM_TYPES = ['gene', 'gene/phenotype', 'phenotype', 'predominantly phenotypes', 'moved/removed']

PHENOTYPE_SYMBOL_EXPLAIN = {
    '[ ]': 'indicate "nondiseases," mainly genetic variations that lead to apparently abnormal laboratory test values',
    '{ }': 'indicate mutations that contribute to susceptibility to multifactorial disorders\n(e.g., diabetes, asthma) or to susceptibility to infection',
    '?': 'before the phenotype name indicates that the relationship between the phenotype and gene is provisional.\nMore details about this relationship are provided in the comment field of the map and in the gene and phenotype OMIM entries',
    '(1)': 'the disorder was positioned by mapping of the wildtype gene',
    '(2)': 'the disease phenotype itself was mapped',
    '(3)': 'the molecular basis of the disorder is known',
    '(4)': 'the disorder is a chromosome deletion or duplication syndrome',
}

MIM_PREFIX_EXPLAIN = {
    '*': 'Gene description',
    '+': 'Gene and phenotype, combined',
    '#': 'Phenotype description, molecular basis known',
    '%': 'Phenotype description or locus, molecular basis unknown',
    '': 'Other, mainly phenotypes with suspected mendelian basis',
    '^': 'Moved/Removed',
}
