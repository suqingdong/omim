import click
import prettytable

import omim


@click.command(name='faq', help=click.style('explains of some faq', fg='green'))
def main():
    table1 = prettytable.PrettyTable(['PREFIX', 'EXPLAIN'])
    for k, v in omim.MIM_PREFIX_EXPLAIN.items():
        table1.add_row([k, v])
    table1.align['EXPLAIN'] = 'l'
    click.secho('***** Explains of MIM PREFIX *****', fg='yellow')
    click.secho(str(table1), fg='cyan')

    table2 = prettytable.PrettyTable(['SYMBOL', 'EXPLAIN'])
    for k, v in omim.PHENOTYPE_SYMBOL_EXPLAIN.items():
        table2.add_row([k, v])
    table2.align['EXPLAIN'] = 'l'
    click.secho('***** Explains of PHENOTYPE SYMBOL *****', fg='yellow')
    click.secho(str(table2), fg='cyan')


if __name__ == '__main__':
    main()
