import sys
import json
import datetime

import click
from pygments import highlight, lexers, formatters

from omim import util
from omim.db import OMIM_DATA


__epilog__ = click.style('''

\b
examples:
    omim query -K
    omim query -s hgnc_gene_symbol BMPR2
    omim query -s mim_number 600799
    omim query -s mim_number 600799
    omim query -s geneMap '%Pulmonary hypertension%' -F json -C
''', fg='yellow')

@click.command(name='query',
               help=click.style('query something from database', fg='green'),
               epilog=__epilog__)
@click.option('-K', '--keys', help='list the available keys', is_flag=True)
@click.option('-s', '--search', help='the search string', multiple=True, nargs=2)
@click.option('-l', '--limit', help='limit for output', type=int)
@click.option('-F', '--format', help='the format for output', type=click.Choice(['json', 'tsv']))
@click.option('-o', '--outfile', help='the output filename [stdout]')
@click.option('-C', '--color', help='colorful print for json', is_flag=True)
@click.option('-f', '--fuzzy', help='fuzzy search', is_flag=True)
@click.option('--count', help='count the number of results', is_flag=True)
@click.pass_context
def main(ctx, **kwargs):
    logger = ctx.obj['logger']
    manager = ctx.obj['manager']
    
    limit = kwargs['limit']
    search = kwargs['search']
    fuzzy = kwargs['fuzzy']
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
            if key not in OMIM_DATA.__dict__:
                logger.error(f'invalid key: {key}')
                exit(1)
            
            if fuzzy:
                query = query.filter(OMIM_DATA.__dict__[key].like(value))
            else:
                query = query.filter(OMIM_DATA.__dict__[key] == value)

        if kwargs['count']:
            logger.info(f'{query.count()} results found for your input!')
            exit(0)

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
                
                data = json.dumps(data, indent=2)
                if kwargs['color']:
                    data = highlight(data, lexers.JsonLexer(), formatters.TerminalFormatter())
                out.write(data + '\n')
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
