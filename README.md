# Solmate

Solmate generates convenient and powerful python clients for any Solana program described by an anchor idl.

-----
By embracing code generation, solmate clients are ***just code*** not complex, 
polymorphic library ***magic***. This philosophy drives great UX and powerful features:

**No Magic** - 
See and read the generated client code to understand exactly what’s going on

**IDE Completion** - 
enjoy intelligent autocomplete, suggestions and type checking 

**Customizable** - 
add your own methods directly to generated classes

**Extensible** - 
maybe your smart contract isn’t cookie-cutter, support your contract’s quirks outside of anchor norms by sub-classing `Codegen`

### Usage
```
usage: solmate <...args...>

arguments:
  -h, --help            show this help message and exit
  --idl IDL             Path to idl file
  --addrs ADDRS [ADDRS ...]
  --root-dir ROOT_DIR   Path to output
  --module MODULE       Name of the python module
  --skip-types SKIP_TYPES [SKIP_TYPES ...]
                        Idl types to skip emitting code for
  --default-accounts DEFAULT_ACCOUNTS [DEFAULT_ACCOUNTS ...]
                        Dictionary of account name to public key which are used to 
                        enable default arguments. Must include program_id
  --instruction-tag {anchor,incremental}
                        Type of instruction tag to use. Use 'anchor' if 
                        generating from an anchor idl
  --account-tag {anchor,incremental}
                        Type of account tag to use. Use 'anchor' if 
                        generating from an anchor idl
```

### Installation
Requires `python >= 3.9`
```sh
poetry install solmate
```
or
```sh
pip install solmate
```

### Development Setup

If you want to contribute to Solmate, follow these steps to get set up:

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Install dev dependencies:
```sh
poetry install
```
3. Install [nox-poetry](https://github.com/cjolowicz/nox-poetry) (note: do not use Poetry to install this, see [here](https://medium.com/@cjolowicz/nox-is-a-part-of-your-global-developer-environment-like-poetry-pre-commit-pyenv-or-pipx-1cdeba9198bd))
4. Activate the poetry shell:
```sh
poetry shell
```


[//]: # (Any code outside `LOCK-BEGIN` and `LOCK-END` won’t be overwritten)



