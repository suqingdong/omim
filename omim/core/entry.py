import re
from collections import defaultdict

from omim.core import OMIM


class Entry(OMIM):
    """Entry Parser For Given MIM"""
    def __init__(self, **kwarg):
        super(Entry, self).__init__(**kwarg)

    def parse(self, mim):
        data = defaultdict(list)
        data['mim_number'] = mim

        url = self.omim_url + f'/{mim}'
        soup = self.get_soup(url)

        prefix = soup.select_one('#title').find_next_sibling('div').select_one('.h3 strong')
        prefix = prefix.text if prefix else ''
        data['prefix'] = prefix

        data['title'] = soup.select_one('#preferredTitle').find_next_sibling('h3').text.strip()

        ref = soup.select_one('#referencesFold')

        if ref:
            references = re.findall(r'PubMed: (\d+)', ref.text)
            data['references'] = ', '.join(references)


        for xmap in ('phenotypeMap', 'geneMap'):
            res = soup.select_one(f'#{xmap}')
            if res:
                table = res.parent.select_one('table')
                keys = [th.text.strip() for th in table.select('thead th')]
                keys = [' '.join(key.split()).replace(' Clinical Synopses', '') for key in keys]
                for tr in table.select('tbody tr'):
                    row = [td.text.strip() for td in tr.select('td')]
                    if len(row) == len(keys):
                        values = row
                    else:
                        values = [values[0]] + row
                    context = dict(zip(keys, values))
                    data[xmap].append(context)

        return dict(data)


if __name__ == '__main__':
    from pprint import pprint
    entry = Entry()

    # *
    # data = entry.parse('612367')    # one geneMap
    data = entry.parse('607093')    # one geneMap
    # data = entry.parse('300050')    # no geneMap
    # data = entry.parse('109690')    # multiple geneMap

    # ^
    # data = entry.parse('100500')    # moved
    # data = entry.parse('618428')    # removed

    # data = entry.parse('100650')    # +
    # data = entry.parse('100070')    # %
    # data = entry.parse('100100')    # #
    # data = entry.parse('100050')    # other

    pprint(data)