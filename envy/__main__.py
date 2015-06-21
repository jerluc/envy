import click
import collections
import blessed
import envy.config as config
import envy.commands as commands
import os.path
import sys


runtime = collections.namedtuple('runtime', ['env', 'system_config'])


@click.command()
@click.option('-f', '--force', is_flag=True,
              help='Force initialize the environment')
@click.pass_context
def init(ctx, force):
    commands.init(ctx.obj['runtime'], force)


@click.command()
@click.pass_context
def activate(ctx):
    commands.activate(ctx.obj['runtime'])


@click.command()
@click.pass_context
def deactivate(ctx):
    commands.deactivate(ctx.obj['runtime'])


@click.command()
@click.option('-f', '--force', is_flag=True,
              help='Force destroy the environment')
@click.pass_context
def destroy(ctx, force):
    commands.destroy(ctx.obj['runtime'], force)


@click.group(commands={
    'init': init,
    'activate': activate,
    'deactivate': deactivate,
    'destroy': destroy
})
@click.pass_context
def cli(ctx):
    env = os.path.basename(os.getcwd())
    system_config = config.load_system_config()
    ctx.obj['runtime'] = runtime(env, system_config)
    pass


def main():
    cli(obj={})
