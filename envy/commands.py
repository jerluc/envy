from __future__ import print_function
import envy.config as config
import envy.logger as log

import click

def init(rt, force):
    print(click.style('Initializing environment [%s]' % rt.env, fg='cyan'))


def activate(rt):
    print(click.style('Activating environment [%s]' % rt.env, fg='green'))


def deactivate(rt):
    print(click.style('Deactivating environment [%s]' % rt.env, fg='yellow'))


def destroy(rt, force):
    print(click.style('Destroying environment [%s]' % rt.env, fg='red'))
