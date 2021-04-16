import os
import json
import time
import random

import click

from simple_loggers import SimpleLogger

from omim import version_info, DEFAULT_DB, DEFAULT_URL
from omim.core import OMIM
from omim.core.entry import Entry
from omim.core.update import Update

from omim.db import OMIM_DATA, Manager


@click.group(name='omim', no_args_is_help=True,
             help=click.style(version_info['desc'], fg='green', bold=True))
@click.option('-d', '--dbfile',
              help='the path of database file', default=DEFAULT_DB, show_default=True)
@click.option('-u', '--url',
              help='the url of omim', default=DEFAULT_URL, show_default=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.pass_context
def cli(ctx, **kwargs):
    dbfile = kwargs['database']
    dirname = os.path.dirname(dbfile)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    ctx.ensure_object(dict)
    ctx.obj.update(kwargs)
    ctx.obj['manager'] = Manager(dbfile=dbfile)
    ctx.obj['logger'] = SimpleLogger('OMIM-CLI')
    ctx.obj['entry'] = Entry(omim_url=kwargs['url'])


@cli.command()
@click.pass_context
def update(ctx, **kwargs):
    logger = ctx.obj['logger']

    entry = Entry(omim_url=ctx.obj['url'])

    mim2gene_data = list(entry.parse_mim2gene('mim2gene.txt', mim_types=None))
    total = len(mim2gene_data)

    with ctx.obj['manager'] as manager:
        for n, (mim, context) in enumerate(mim2gene_data):
            logger.debug(f'dealing with: [{n}/{total}] {mim}')
            res = manager.query(OMIM_DATA, 'mim_number', mim)
            if res.first():
                if context['mim_type'] == 'moved/removed':
                    manager.delete(OMIM_DATA, 'mim_number', mim)
                else:
                    click.secho(f'*** skip: {mim}', fg='yellow')
                continue

            data = entry.parse(mim)
            context.update(data)
            temp_dict = {
                k: json.dumps(v) if isinstance(v, list) else v 
                for k, v in context.items()
            }
            omim_data = OMIM_DATA(**temp_dict)
            manager.insert(OMIM_DATA, 'mim_number', omim_data)

            time.sleep(random.randint(6, 10))


@cli.command()
@click.option('-m', '--mim', help='the mim number to search', required=True)
@click.pass_context
def crawl(ctx, **kwargs):
    entry = Entry(omim_url=ctx.obj['url'])
    data = entry.parse(kwargs['mim'])
    print(json.dumps(data, indent=2))


def main():
    cli()


if __name__ == '__main__':
    main()
