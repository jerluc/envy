# Envy

Envy allows developers to simply create project-based development environments that enable flexible
configuration of environmental variables and macros.

## Installation

```
pip install envy
```

## Shell completion

Since envy uses the Python click module, you can add the following to your shell profile file to
incorporate project-specific completions:

```shell
# For bash, add the following to your shell profile (e.g. .bashrc)
eval "$(_NV_COMPLETE=source_bash nv)"

# For zsh, add the following to your shell profile (e.g. .zshrc)
eval "$(_NV_COMPLETE=source_zsh nv)"
```
