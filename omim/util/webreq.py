import requests
from webrequests import WebRequest as WR


def get_response(url, proxy=False, **kwargs):
    proxies = None
    if proxy:
        proxies = {'http': f'http://{proxy}'}
        print(f'use proxies: {proxies}')

    resp = WR.get_response(url, proxies=proxies, timeout=5, max_try=1, **kwargs)
    print(resp.text)


if __name__ == '__main__':

    proxy_pool_url = False
    proxy_pool_url = 'http://127.0.0.1:5010/'

    url = 'https://www.omim.org/statistics/update'
    url2 = 'https://mirror.omim.org/statistics/update'

    # get_response(url, proxy='127.0.0.1:10802')
    get_response(url)
