import click
import sys
import typing

from envy import __version__, env as nvenv

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def main():
    # Firstly, create the command group
    @click.group(chain=True, context_settings=CONTEXT_SETTINGS)
    @click.version_option(version=__version__, prog_name="nv")
    def cli():
        pass

    # Load the environment
    env = nvenv.load()

    def add_cli_command(
        group: click.Group,
        command_name: str,
        fn: typing.Callable[..., int],
        *fnargs: typing.Any
    ):
        """
        Helper function to dynamically add a new CLI command to a group
        """
        cli_command = group.command(command_name)

        def command_func():
            exitcode = fn(*fnargs)
            sys.exit(exitcode)

        cli_command(command_func)

    # Add user-defined macro commands
    for macro in env.macros:
        add_cli_command(cli, macro, env.run, macro)

    # Add builtin command for printing variables
    @cli.command("vars")
    @click.argument("variable_name", type=click.Choice(env.vars))
    def printvar(variable_name: str):
        print(env.getvar(variable_name))

    # Finally, run the CLI
    cli()
