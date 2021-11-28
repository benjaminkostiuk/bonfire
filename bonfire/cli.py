import click
from tabulate import tabulate

from .exceptions import BonfireNotFound
from .process import find_running_apps, open_application
from .db import list_bonfires, save_bonfire, delete_bonfire, find_bonfire_by_id, find_bonfire_by_nickname, rename_bonfire
from .fire import Fire

# Command line interface
class Cmd:
    def __init__(self):
        self.quiet = False
        self.verbose = False
    
    def set_context(self, ctx):
        self.quiet = ctx['quiet']
        self.verbose = ctx['verbose']
    
    def echo(self, msg):
        if not self.quiet or self.verbose:
            click.echo(msg)
    
    def vecho(self, msg):
        if self.verbose:
            click.echo(msg)

cmd = Cmd()

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
    cmd.set_context(ctx.obj)

# Command: bonfire light [OPTIONS] [NICKNAME]
@cli.command(name='light')
@click.argument('nickname', required=False)
@click.pass_context
def light(ctx, nickname):
    '''
    Light a bonfire saving application state. Optionally give the bonfire a nickname.
    '''
    cmd.echo('Chopping up wood 🪓')
    running_apps = find_running_apps()
    # Echo all proceses found if verbose
    if ctx.obj['verbose']:
        for process in running_apps:
            cmd.vecho('Found process {} with exec path {}'.format(process, running_apps[process]['path']))
    # Build and save a bonfire
    bonfire = Fire(running_apps, nickname=nickname)
    save_bonfire(bonfire)
    cmd.echo("Bonfire lit 🔥")

# Command: bonfire restore [OPTIONS] ID
@cli.command(name='restore')
@click.argument('id')
@click.option('--use-name', '-n', is_flag=True, help='Use the bonfire nickname instead of the id')
@click.pass_context
def restore(ctx, id, use_name):
    '''
    Restore to a bonfire save point.
    '''
    try:
        lit_bonfire = find_bonfire_by_nickname(id) if use_name else find_bonfire_by_id(id)
    except BonfireNotFound:
        cmd.echo('Could not find bonfire with {} {}'.format('nickname' if use_name else 'id', id))
        exit(1)
    
    cmd.vecho('Found bonfire with id {}, nickname {}, with {} processes.'.format(lit_bonfire.id, lit_bonfire.nickname, len(lit_bonfire.apps)))
    cmd.echo('Rekindling bonfire ✨')
    for process in lit_bonfire.apps:
        cmd.vecho('Starting process {} with exec path: {}'.format(process, lit_bonfire.apps[process]))
        open_application(process, lit_bonfire.apps[process])
    cmd.echo('Bonfire rekindled 🔥')

# Command: bonfire list [OPTIONS]
@cli.command(name='list')
@click.pass_context
def list(ctx):
    '''
    List lit bonfires.
    '''
    bonfires = [fire.rattrs() for fire in list_bonfires()]
    if not bonfires:
        cmd.echo('No bonfires.')
    else:
        cmd.echo(tabulate(bonfires, headers=Fire.attrs()))

# Command: bonfire rename [OPTIONS] ID NICKNAME
# Rename a bonfire identified by ID with name NICKNAME
@cli.command(name='rename')
@click.argument('id')
@click.argument('nickname')
@click.pass_context
def rename(ctx, id, nickname):
    '''
    Rename a bonfire.
    '''
    try:
        bonfire_to_rename = find_bonfire_by_id(id)
    except BonfireNotFound:
        cmd.echo('No bonfire with id {}'.format(id))
        exit(1)
    rename_bonfire(bonfire_to_rename, nickname)
    cmd.echo('Bonfire {} [{} --> {}]'.format(bonfire_to_rename.id, bonfire_to_rename.nickname, nickname))

# Command: bonfire extinguish [OPTIONS] [IDS]...
# Extinguish one or more bonfires identified by IDS
@cli.command(name='extinguish')
@click.argument('ids', nargs=-1)
@click.pass_context
def extinguish(ctx, ids):
    '''
    Extinguish a bonfire, deleting the save point.
    '''
    ids_to_delete = [id for id in ids]
    if not ids_to_delete:
        cmd.echo("Error: Missing argument 'ID'.")
        exit(1)
    try:
        delete_bonfire(ids_to_delete)
    except BonfireNotFound:
        cmd.echo('Failed to find all bonfires with ids {}'.format(ids_to_delete))
        exit(1)
    cmd.echo("Bonfire{} extinguished 💨".format('s' if len(ids) > 1 else ''))

if __name__ == '__main__':
    cli()