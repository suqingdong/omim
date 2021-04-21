import os

import click
from simple_loggers import SimpleLogger

from omim import version_info, DEFAULT_DB, DEFAULT_URL
from omim.core.entry import Entry
from omim.db import Manager

from ._update import main as update_cli
from ._query import main as query_cli
from ._stats import main as stats_cli
from ._faq import main as faq_cli


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])

@click.group(name='omim', no_args_is_help=True,
             context_settings=CONTEXT_SETTINGS,
             help=click.style(version_info['desc'], fg='green', bold=True))
@click.option('-d', '--dbfile',
              help='the path of database file', default=DEFAULT_DB, show_default=True)
@click.option('-u', '--url',
              help='the url of omim', default=DEFAULT_URL, show_default=True)
@click.option('--echo', help='turn on echo', hidden=True, is_flag=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.pass_context
def cli(ctx, **kwargs):
    dbfile = kwargs['dbfile']
    dirname = os.path.dirname(dbfile)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    ctx.ensure_object(dict)

    ctx.obj['manager'] = Manager(dbfile=dbfile, echo=kwargs['echo'])
    ctx.obj['logger'] = SimpleLogger('OMIM-CLI')
    ctx.obj['entry'] = Entry(omim_url=kwargs['url'])


def main():
    cli.add_command(update_cli)
    cli.add_command(query_cli)
    cli.add_command(stats_cli)
    cli.add_command(faq_cli)
    cli()


if __name__ == '__main__':
    main()
