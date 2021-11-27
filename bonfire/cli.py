import click
from .process import find_all_processes
from .config import config
from .db import Fire, list_bonfires, save_bonfire, delete_bonfire
from tabulate import tabulate

# Base command group
@click.group()
@click.option('--quiet', '-q', is_flag=True, help='Silence the output')
@click.option('--verbose', '-v', is_flag=True, help='Make the output verbose')
@click.pass_context
def cli(ctx, quiet, verbose):
    ctx.obj = {
        'quiet': quiet,
        'verbose': verbose
    }

# Command: bonfire light [OPTIONS] [NICKNAME]
# Optionally provide a nickname for the bonfire
@cli.command(name='light')
@click.argument('nickname', required=False)
@click.pass_context
def light(ctx, nickname):
    '''
    Light a bonfire saving application state
    '''
    new_fire = Fire([], nickname=nickname)
    save_bonfire(new_fire)
    if not ctx.obj['quiet']:
        click.echo("Bonfire lit 🔥")

# Command: Restore
@cli.command(name='restore')
@click.pass_context
def restore(ctx):
    '''
    Restore application state to a bonfire save point
    '''
    pass

# Command: bonfire list [OPTIONS]
@cli.command(name='list')
@click.pass_context
def list(ctx):
    '''
    List lit bonfires
    '''
    # Possible show all here if verbose
    bonfires = [fire.rattrs() for fire in list_bonfires()]
    if not bonfires:
        click.echo('No bonfires')
    else:
        click.echo(tabulate(bonfires, headers=Fire.attrs()))

# Command: Rename
@cli.command(name='rename')
@click.argument('bonfire')
@click.argument('name')
@click.pass_context
def rename(ctx, bonfire, name):
    '''Rename a bonfire'''
    pass

# Command: Extinguish
@cli.command(name='extinguish')
@click.argument('bonfire')
@click.pass_context
def extinguish(ctx, bonfire):
    '''
    Extinguish a bonfire, deleting the save point
    '''
    bonfires_smothered = delete_bonfire(bonfire)
    if not bonfires_smothered:
        click.echo('No bonfires matching {}'.format(bonfire))
    else:
        click.echo("Bonfire extinguished 💨")

if __name__ == '__main__':
    cli()
