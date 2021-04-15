import click

from omim import version_info
from omim.core import OMIM
from omim.core.entry import Entry
from omim.core.update import Update


@click.group(name='omim')
def cli(**kwargs):
    pass


@cli.command()
def update(**kwargs):
    pass


@cli.command()
def query(**kwargs):
    pass


def main():
    cli()


if __name__ == '__main__':
    main()
