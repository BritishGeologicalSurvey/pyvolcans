# Open-access VOLCANS

Collaborative effort to create an free-software (Python), open-access version of VOLCANS (https://doi.org/10.1007/s00445-019-1336-3). 1st stage: provide the users with results from VOLCANS. 2nd stage: clean, re-test and open the whole VOLCANS code

## Installation

`pyvolcans` can be imported to a new environment as follows:

```
pip install git+https://gitlab.com/PTierz/pyvolcans.git
```

It is necessary to have git installed and on the system path.  You will be
asked for your GitLab username and password.

This method adds `pyvolcans` to the virtual environment PATH so that it can be
used from any directory.


## Local development setup

In a clean virtual environment, run the following from the root directory of
the project to install `pyvolcans` in development mode.

```bash
python -m pip install -e .[dev]
```

The `-e` flag makes the files in the current working directory available
throughout the virtual environment and so changes are reflected straight away.
With this installation, it is no longer required to set the PYTHONPATH.

The `[dev]` part installs packages required for development e.g. `pytest`.

Run tests with:

```bash
pytest -vs test
```
