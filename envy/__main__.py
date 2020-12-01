import click

from envy import __version__, env as nvenv

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def main():
    @click.group(chain=True, context_settings=CONTEXT_SETTINGS)
    @click.version_option(version=__version__, prog_name="envy")
    def cli():
        pass

    env = nvenv.load()

    def add_macro_cli(macro: str):
        @cli.command(macro)
        def macro_command():
            print(f"Running macro: {macro}")
            env.run(macro)

    for macro in env.macros.keys():
        add_macro_cli(macro)

    cli()
