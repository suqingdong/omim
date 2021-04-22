import click

from omim import util


@click.command(name='stats', help=click.style('statistics of the database', fg='green'))
@click.pass_context
def main(ctx, **kwargs):
    manager = ctx.obj['manager']

    generated, table = util.get_stats_table(manager)

    click.secho(f'***** updated time: {generated} *****', fg='yellow', bold=True)
    click.secho(str(table), fg='cyan', bold=True)


if __name__ == '__main__':
    main()
