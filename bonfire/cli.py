import click

# Base command group
@click.group()
@click.option('--quiet', '-q', is_flag=True, help='Silence the output')
@click.option('--verbose', '-v', is_flag=True, help='Make the output verbose')
@click.pass_context
def cli(ctx, quiet, verbose):
    ctx.obj = {}
    ctx.obj['quiet'] = quiet

# Command: Light
@cli.command(name='light')
@click.pass_context
def light(ctx):
    '''Light a bonfire saving application state'''
    print(ctx.obj)
    if ctx:
        click.echo("Quietly")
    click.echo("Lighting")

# Command: Restore
@cli.command(name='restore')
@click.pass_context
def restore(ctx):
    '''Restore application state to a bonfire save point'''
    pass

# Command: List
@cli.command(name='list')
@click.pass_context
def list(ctx):
    '''List lit bonfires'''
    pass

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
    '''Extinguish a bonfire, deleting the save point'''
    print(bonfire)
    pass

if __name__ == '__main__':
    cli()
