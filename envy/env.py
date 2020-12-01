import os
import os.path
import pathlib
import shlex
import subprocess
import typing
import yaml

from pydantic import BaseModel, BaseSettings, FilePath, PyObject

from .macro.cmd import CommandRunner


CONFIG_FILE_NAME = ".envy.yml"

Vars = typing.Mapping[str, str]
VarsOrEnvFile = typing.Union[FilePath, Vars]
MacroType = typing.Union[FilePath, PyObject, str]
Macros = typing.Mapping[str, MacroType]


class Environment(BaseModel):
    vars: Vars
    macros: Macros

    def extend(self, other: "Environment") -> "Environment":
        return Environment(
            vars={**other.vars, **self.vars}, macros={**other.macros, **self.macros}
        )

    def run(self, macro: str) -> int:
        if macro not in self.macros:
            raise KeyError(f"Undefined macro: '{macro}'")
        return self.macros[macro]()


def _pyobj_runner(pyobj: PyObject) -> typing.Callable[[], int]:
    def runner() -> int:
        assert callable(pyobj)
        pyobj()
        return 0


class EnvyConfig(BaseSettings):
    vars: typing.Optional[VarsOrEnvFile] = {}
    macros: typing.Optional[Macros] = {}

    def to_environment(self) -> Environment:
        vars: Vars = {}
        if isinstance(self.vars, dict):
            vars = self.vars
        elif isinstance(self.vars, FilePath):
            pass

        macros: Macros = {}
        for name, mfn in self.macros.items():
            if callable(mfn):
                macros[name] = mfn
            elif isinstance(mfn, pathlib.Path):
                # TODO: Should the path be relative to the environment file location?
                macros[name] = CommandRunner(str(mfn)).run
            else:
                macros[name] = CommandRunner(mfn).run

        return Environment(vars=vars, macros=macros)


def load_env(config_file_path: str) -> Environment:
    with open(config_file_path) as config_file:
        raw_config = yaml.load(config_file, yaml.SafeLoader) or {}
        return EnvyConfig.parse_obj(raw_config).to_environment()


def load() -> Environment:
    cwd = pathlib.Path(os.path.abspath(os.getcwd()))
    env = Environment(vars={}, macros={})
    search_dirs = list(cwd.parents)[::-1] + [cwd]
    for dir in search_dirs:
        config_file_path = os.path.join(dir, CONFIG_FILE_NAME)
        if os.path.exists(config_file_path):
            env = env.extend(load_env(config_file_path))
    return env
