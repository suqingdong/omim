import json
import time
import random

import click

from omim.db import OMIM_DATA, Manager


MIM_TYPES = ['gene', 'gene/phenotype', 'moved/removed', 'phenotype', 'predominantly phenotypes']

@click.command(name='update')
@click.option('-t', '--mim-types', help='the types of mim crawl',
              type=click.Choice(MIM_TYPES), show_choices=True, multiple=True)
@click.pass_context
def main(ctx, **kwargs):
    logger = ctx.obj['logger']
    entry = ctx.obj['entry']
    manager = ctx.obj['manager']
    
    logger.debug(f'input arguments: {kwargs}')

    mim_types = kwargs['mim_types']

    mim2gene_data = list(entry.parse_mim2gene('mim2gene.txt', mim_types=mim_types))
    total = len(mim2gene_data)

    with manager:
        for n, (mim, context) in enumerate(mim2gene_data, 1):
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


if __name__ == '__main__':
    main()
