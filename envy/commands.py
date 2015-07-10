# -*- coding: utf-8 -*-

from __future__ import print_function
from envy.env import Environment, ConfigurationException
import envy.logger as log
import click
import os
import subprocess
import sys

def init(basedir, recreate):
    env = Environment(basedir)

    if recreate:
        confirmation = click.style('Are you sure you want to re-initialize this workspace? This will delete any pre-existing workspace!', fg='red')
        if click.confirm(confirmation):
            env.destroy()
        else:
            return 1

    print(click.style('Initializing workspace [%s]' % env.name, fg='cyan'))

    env.init(autocreate=True)

    return 0


def enter(basedir):
    if 'ENVY' in os.environ:
        print(click.style('Cannot enter a workspace while another workspace is already active', fg='red'))
        return 1

    try:
        env = Environment(basedir)
        env.init(autocreate=False)
    except ConfigurationException as e:
        print(click.style(e.message, fg='red'))
        return 1

    print(click.style('Entering workspace [%s]; use "exit" to leave this workspace' % env.name, fg='green'))

    shell_env = os.environ.copy()
    shell_env['ENVY'] = env.name
    shell_env['ENVY_DIR'] = env.config.location
    shell_env['ENVY_SYS_DIR'] = env.system_config.location
    shell_env['ENVY_PROMPT'] = '%s ⚡ ' % click.style(env.name, fg='cyan', bold=True)
    init_file = os.path.join(env.config.location, 'bin', 'init')
    return subprocess.call([os.environ['SHELL'], '--init-file', init_file], env=shell_env)


def destroy(basedir, force):
    if not force:
        confirmation = click.style('Are you sure you want to destroy this workspace?', fg='red')
        if not click.confirm(confirmation):
            return 1

    try:
        env = Environment(basedir)
        env.init(autocreate=False)
    except ConfigurationException as e:
        print(click.style(e.message, fg='red'))
        return 1

    print(click.style('Destroying workspace [%s]' % env.name, fg='red'))
    env.destroy()

    return 0
