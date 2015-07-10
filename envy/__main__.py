# -*- coding: utf-8 -*-

import click
import collections
import blessed
import envy.commands as commands
import os.path
import sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CWD = os.path.abspath(os.getcwd())


def _maybe_exit(exit_code):
    if exit_code > 0:
        sys.exit(exit_code)


@click.group(chain=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0-alpha', prog_name='envy')
def cli():
    pass


@cli.command('i')
@click.option('-r', '--recreate', is_flag=True,
              help='Re-initialize the workspace')
def init(recreate):
    """Initializes a new workspace"""
    _maybe_exit(commands.init(CWD, recreate))


@cli.command('e')
def enter():
    """Enters the current workspace"""
    _maybe_exit(commands.enter(CWD))


@cli.command('d')
@click.option('-f', '--force', is_flag=True,
              help='Force destroy the workspace')
def destroy(force):
    """Destroys the current workspace"""
    _maybe_exit(commands.destroy(CWD, force))


def main():
    cli()
