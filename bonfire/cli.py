import click

from bonfire.exceptions import BonfireNotFound
from .process import find_running_apps, open_application
from .config import config
from .db import list_bonfires, save_bonfire, delete_bonfire, find_bonfire_by_id, find_bonfire_by_nickname, rename_bonfire
from .fire import Fire
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
    if not ctx.obj['quiet']:
        click.echo('Chopping up wood 🪓')
    running_apps = find_running_apps()
    # Echo all proceses found if verbose
    if ctx.obj['verbose']:
        for process in running_apps:
            click.echo('Found process {} with exec path {}'.format(process, running_apps[process]))
    # Build and save a bonfire
    bonfire = Fire(running_apps, nickname=nickname)
    save_bonfire(bonfire)
    if not ctx.obj['quiet']:
        click.echo("Bonfire lit 🔥")

# Command: Restore
@cli.command(name='restore')
@click.argument('identifier')
@click.pass_context
def restore(ctx, identifier):
    '''
    Restore application state to a bonfire save point
    '''
    try:
        lit_bonfire = find_bonfire_by_nickname(identifier)
    except BonfireNotFound as e:
        if not ctx.obj['quiet']:
            click.echo('Could not find bonfire for nickname or id {}'.format(identifier))
            exit(1)
    click.echo('Rekindling bonfire 🎇')
    for process in lit_bonfire.apps:
        open_application(process, lit_bonfire.apps[process])
    click.echo('Bonfire rekindled 🔥')

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

# Command: bonfire rename [OPTIONS] ID NICKNAME
# Rename a bonfire identified by ID with name NICKNAME
@cli.command(name='rename')
@click.argument('id')
@click.argument('nickname')
@click.pass_context
def rename(ctx, id, nickname):
    '''
    Rename a bonfire
    '''
    bonfire_to_rename = find_bonfire_by_id(id)
    if not bonfire_to_rename and not ctx.obj['quiet']:
        click.echo('No bonfire with id {}'.format(id))
        exit(1)
    rename_bonfire(bonfire_to_rename, nickname)
    if not ctx.obj['quiet']:
        click.echo('Bonfire {} [{} --> {}]'.format(bonfire_to_rename.id, bonfire_to_rename.nickname, nickname))

# Command: bonfire extinguish [OPTIONS] [IDS]...
# Extinguish one or more bonfires identified by IDS
@cli.command(name='extinguish')
@click.argument('ids', nargs=-1)
@click.pass_context
def extinguish(ctx, ids):
    '''
    Extinguish a bonfire, deleting the save point
    '''
    ids_to_delete = [id for id in ids]
    bonfire_smothered = delete_bonfire(ids_to_delete)
    if not bonfire_smothered:
        click.echo('Failed to find all bonfires with ids {}'.format(ids_to_delete))
        exit(1)
    if not ctx.obj['quiet']:
        click.echo("Bonfire{} extinguished 💨".format('s' if len(ids) > 1 else ''))

if __name__ == '__main__':
    cli()
