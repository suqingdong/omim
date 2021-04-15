import re
from collections import defaultdict

from dateutil.parser import parse
from dateutil import rrule

from omim.core import OMIM


class Update(OMIM):
    """OMIM Update List"""
    def __init__(self, **kwarg):
        super(Update, self).__init__(**kwarg)

    def check(self, year, month):
        url = self.omim_url + f'/statistics/updates/{year}/{month}'
        soup = self.get_soup(url)
        for row in soup.select('#content div:nth-child(1) .row'):
            h4 = row.select_one('h4')
            a = row.select_one('div a')
            strong = row.select_one('strong')
            if h4:
                print('*** update date:', h4.text.strip())
            elif a:
                print('>>> item:', a.text.strip())
            elif strong:
                print('### type', strong.text.strip())
            




if __name__ == '__main__':
    update = Update()
    update.check(2021, 3)
