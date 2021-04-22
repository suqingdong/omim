import sys
import json
import datetime

import click

from omim import util
from omim.db import OMIM_DATA


@click.command(name='query', help=click.style('query something from database', fg='green'))
@click.option('-K', '--keys', help='list the available keys', is_flag=True)
@click.option('-s', '--search', help='the search string', multiple=True, nargs=2)
@click.option('-l', '--limit', help='limit for output', type=int)
@click.option('-F', '--format', help='the format for output', type=click.Choice(['json', 'tsv']))
@click.option('-o', '--outfile', help='the output filename [stdout]')
@click.pass_context
def main(ctx, **kwargs):
    logger = ctx.obj['logger']
    manager = ctx.obj['manager']
    
    limit = kwargs['limit']
    search = kwargs['search']
    out = open(kwargs['outfile'], 'w') if kwargs['outfile'] else sys.stdout

    logger.debug(f'input arguments: {kwargs}')

    if kwargs['keys']:
        table = util.get_columns_table()
        print(click.style(str(table), fg='cyan'))
        exit(0)

    if not search:
        logger.warning('please query something with -s/--search argument')
        exit(1)

    with manager:
        query = manager.session.query(OMIM_DATA)

        for key, value in search:
            if '%' in value:
                query = query.filter(OMIM_DATA.__dict__[key].like(value))
            else:
                query = query.filter(OMIM_DATA.__dict__[key] == value)

        if limit:
            query = query.limit(limit)

    if not query.count():
        logger.warning(f'no result for your input! [{search}]')
    else:
        with out:
            if kwargs['format'] == 'json':
                data = []
                for each in query.all():
                    context = {}
                    for k, v in each.as_dict.items():
                        if v:
                            if k in ('geneMap', 'phenotypeMap'):
                                v = json.loads(v)
                            elif k == 'generated':
                                v = v.strftime('%Y-%m-%d')
                        context[k] = v
                    data.append(context)
                out.write(json.dumps(data, indent=2) + '\n')
            else:
                for n, each in enumerate(query.all()):
                    context = each.as_dict
                    if n == 0:
                        title = '\t'.join(context.keys())
                        out.write(title + '\n')
                    line = '\t'.join([
                        v.strftime('%Y-%m-%d') if isinstance(v, datetime.datetime) else str(v)
                        for v in context.values()])
                    out.write(line + '\n')


if __name__ == '__main__':
    main()
