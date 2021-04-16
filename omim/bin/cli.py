import os

import click

from simple_loggers import SimpleLogger

from omim import version_info, DEFAULT_DB, DEFAULT_URL
from omim.core import OMIM
from omim.core.entry import Entry
from omim.core.update import Update

from omim.db import OMIM_DATA, Manager

from ._update import main as update_cli

@click.group(name='omim', no_args_is_help=True,
             help=click.style(version_info['desc'], fg='green', bold=True))
@click.option('-d', '--dbfile',
              help='the path of database file', default=DEFAULT_DB, show_default=True)
@click.option('-u', '--url',
              help='the url of omim', default=DEFAULT_URL, show_default=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.pass_context
def cli(ctx, **kwargs):
    dbfile = kwargs['dbfile']
    dirname = os.path.dirname(dbfile)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    ctx.ensure_object(dict)

    ctx.obj['manager'] = Manager(dbfile=dbfile)
    ctx.obj['logger'] = SimpleLogger('OMIM-CLI')
    ctx.obj['entry'] = Entry(omim_url=kwargs['url'])


def main():
    cli.add_command(update_cli)
    cli()


if __name__ == '__main__':
    main()
