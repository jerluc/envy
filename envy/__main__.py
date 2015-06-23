import click
import collections
import blessed
import envy.commands as commands
import os.path
import sys


@click.command()
@click.option('-e', '--enter', is_flag=True,
              help='Enter the workspace after intializing')
@click.option('-r', '--recreate', is_flag=True,
              help='Re-initialize the workspace')
@click.pass_context
def init(ctx, enter, recreate):
    sys.exit(commands.init(ctx.obj['basedir'], enter, recreate))


@click.command()
@click.pass_context
def enter(ctx):
    sys.exit(commands.enter(ctx.obj['basedir']))


@click.command()
@click.option('-f', '--force', is_flag=True,
              help='Force destroy the workspace')
@click.pass_context
def destroy(ctx, force):
    sys.exit(commands.destroy(ctx.obj['basedir'], force))


@click.group(commands={
    'init': init,
    'enter': enter,
    'destroy': destroy
})
@click.pass_context
def cli(ctx):
    ctx.obj['basedir'] = os.path.abspath(os.getcwd())
    pass


def main():
    cli(obj={})
