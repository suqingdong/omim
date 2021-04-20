import click
import prettytable

from omim import MIM_TYPES
from omim.db import OMIM_DATA


@click.command(name='query', help=click.style('query something from database', fg='green'))
@click.option('-K', '--keys', help='list the available keys', is_flag=True)
@click.option('-s', '--search', help='the search string', multiple=True, nargs=2)
@click.option('-l', '--limit', help='limit for output', type=int)
@click.option('-o', '--outfile', help='the output filename [stdout]')
@click.pass_context
def main(ctx, **kwargs):
    logger = ctx.obj['logger']
    manager = ctx.obj['manager']
    
    limit = kwargs['limit']
    search = kwargs['search']

    logger.debug(f'input arguments: {kwargs}')

    if kwargs['keys']:
        table = prettytable.PrettyTable(['Key', 'Comment', 'Type'])
        for k, v in OMIM_DATA.metadata.tables['omim'].columns.items():
            table.add_row([k, v.comment, v.type])
        for field in table._field_names:
            table.align[field] = 'l'
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

        # logger.debug(str(query))

    if not query.count():
        logger.warning('no result for your input!')
    else:
        for each in query.all():
            print(each.as_dict)


if __name__ == '__main__':
    main()
