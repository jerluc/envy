import os
import os.path
import pathlib
import typing
import yaml

from pydantic import BaseSettings, FilePath, PyObject

from .macro import MacroProto, shell, py


CONFIG_FILE_NAME = ".envy.yml"

Vars = typing.Mapping[str, str]
VarsOrEnvFile = typing.Union[FilePath, Vars]
MacroType = typing.Union[FilePath, PyObject, str]
Macros = typing.Mapping[str, MacroType]
RunnableMacros = typing.Mapping[str, MacroProto]


class Environment:
    def __init__(
        self,
        vars: Vars,
        macros: RunnableMacros,
        parent: typing.Optional["Environment"] = None,
    ):
        self._vars = vars
        self._macros = macros
        self._parent = parent

    @property
    def vars(self) -> typing.Iterable[str]:
        vars = list(self._vars.keys())
        if self._parent is not None:
            vars += self._parent.vars
        return set(vars)

    @property
    def macros(self) -> typing.Iterable[str]:
        macros = list(self._macros.keys())
        if self._parent is not None:
            macros += self._parent.macros
        return set(macros)

    def extend(self, parent: "Environment") -> "Environment":
        """
        Links this environment to its parent
        """
        self._parent = parent
        return self

    def getvar(self, variable_name: str) -> str:
        """
        Retrieves a variable by name
        """
        if variable_name not in self._vars:
            if self._parent is not None:
                return self._parent.getvar(variable_name)
            raise KeyError(f"Undefined variable: '{variable_name}'")
        return self._vars[variable_name]

    def run(self, macro: str) -> int:
        """
        Runs a macro by name
        """
        if macro not in self._macros:
            if self._parent is not None:
                return self._parent.run(macro)
            raise KeyError(f"Undefined macro: '{macro}'")
        return self._macros[macro].run()


class EnvyConfig(BaseSettings):
    vars: typing.Optional[VarsOrEnvFile] = {}
    macros: typing.Optional[Macros] = {}

    def to_environment(self) -> Environment:
        """
        Hydrates an executable envy environment from a parsed configuration file
        """
        vars: Vars = {}
        if isinstance(self.vars, dict):
            vars = self.vars
        elif isinstance(self.vars, FilePath):
            pass

        macros: typing.Dict[str, MacroProto] = {}
        if self.macros:
            for name, mfn in self.macros.items():
                if callable(mfn):
                    macros[name] = py.PyMacro(mfn)
                elif isinstance(mfn, pathlib.Path):
                    # TODO: Should the path be relative to the environment file location?
                    macros[name] = shell.ShellMacro(str(mfn), spawn_subshell=False)
                elif isinstance(mfn, str):
                    macros[name] = shell.ShellMacro(mfn)
                else:
                    raise TypeError(f"Unsupported macro: {mfn}")

        return Environment(vars, macros)


def _load_env(config_file_path: pathlib.Path) -> Environment:
    """
    Loads and parses an envy environment from a file path
    """
    with open(config_file_path) as config_file:
        raw_config = yaml.load(config_file, yaml.SafeLoader) or {}
        return EnvyConfig.parse_obj(raw_config).to_environment()


def load() -> Environment:
    """
    Loads the effective envy environment from the current working directory
    """
    cwd = pathlib.Path(os.path.abspath(os.getcwd()))
    env = Environment({}, {})

    # Start from the root directory, and recursively extend to the current working directory
    search_dirs = list(cwd.parents) + [cwd]
    for dir in search_dirs:
        config_file_path = pathlib.Path(os.path.join(dir, CONFIG_FILE_NAME))
        # If a .envy.yml file exists
        if os.path.exists(config_file_path):
            # Load the envy configuration
            this_env = _load_env(config_file_path)
            # And extend it
            env = this_env.extend(env)

    return env
