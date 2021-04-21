import os
import json
import time
import random
import datetime

import click

from omim import MIM_TYPES
from omim.db import OMIM_DATA


@click.command(name='update', help=click.style('update the database', fg='green'))
@click.option('-t', '--mim-types', help='the types of mim crawl',
              type=click.Choice(MIM_TYPES), show_choices=True, multiple=True)
@click.option('-m', '--mim2gene', help='download the mim2gene.txt file firstly', default='mim2gene.txt', show_default=True)
@click.pass_context
def main(ctx, **kwargs):
    logger = ctx.obj['logger']
    entry = ctx.obj['entry']
    manager = ctx.obj['manager']

    logger.debug(f'input arguments: {kwargs}')

    mim_types = kwargs['mim_types']
    mim2gene = kwargs['mim2gene']

    need_update = True
    if mim2gene and os.path.isfile(mim2gene):
        now_time = datetime.datetime.now()
        file_time = datetime.datetime.fromtimestamp(os.stat(mim2gene).st_ctime)
        need_update = (file_time.year, file_time.month, file_time.day) != (now_time.year, now_time.month, now_time.day)

    if need_update:
        logger.debug(f'update mim2gene: {mim2gene}')
        entry.get_mim2gene(outfile=mim2gene)

    mim2gene_data = list(entry.parse_mim2gene(mim2gene, mim_types=mim_types))
    total = len(mim2gene_data)

    with manager:
        for n, (mim, context) in enumerate(mim2gene_data, 1):
            logger.debug(f'dealing with: [{n}/{total}] {mim}')
            res = manager.query(OMIM_DATA, 'mim_number', mim)
            if res.first() and context['mim_type'] == res.first().mim_type:
                click.secho(f'*** skip mim_number: {mim}', fg='yellow')
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


if __name__ == '__main__':
    main()
