from omim.core import OMIM
import click
import prettytable

from omim import MIM_TYPES
from omim.db import OMIM_DATA


@click.command(name='stats', help=click.style('statistics of the database', fg='green'))
@click.pass_context
def main(ctx, **kwargs):
    manager = ctx.obj['manager']

    with manager:

        query = manager.query(OMIM_DATA)
        generated = query.order_by(OMIM_DATA.generated.desc()).first().generated.strftime('%Y-%m-%d')

        total = 0
        table = prettytable.PrettyTable(['MIM_TYPE', 'COUNT'])
        for mim_type in MIM_TYPES:
            res = manager.query(OMIM_DATA, 'mim_type', mim_type)
            table.add_row([mim_type, res.count()])
            total += res.count()

        table.add_row(['TOTAL COUNT', total])
        table.align['MIM_TYPE'] = 'l'
        table.align['COUNT'] = 'l'

    click.secho(f'***** updated time: {generated} *****', fg='yellow', bold=True)
    click.secho(str(table), fg='cyan', bold=True)


if __name__ == '__main__':
    main()
