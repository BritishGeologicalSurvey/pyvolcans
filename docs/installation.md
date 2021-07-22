# Installation 

PyVOLCANS can be installed from PyPI as follows:

```
pip install pyvolcans
```

This method adds `pyvolcans` to the virtual environment PATH so that it can be
used from any directory.

## Installation for Developers

To modify the code, first clone the PyVOLCANS repository into your local machine:

```bash
git clone https://github.com/BritishGeologicalSurvey/pyvolcans
```

Then move to the root directory of the project (`pyvolcans`, which contains the `setup.py` file - 
please also check the `requirements.txt` file for a full list of dependencies in the code),
and run the following command to install PyVOLCANS in development mode, preferably within a
clean virtual environment:

```bash
python -m pip install -e .[dev]
```

The `-e` flag makes the files in the current working directory available
throughout the virtual environment and, therefore, changes are reflected straight away.
With this installation, it is no longer required to set the PYTHONPATH.

The `[dev]` part installs packages required for development e.g. `pytest`.

Run tests with:

```bash
pytest -v test
```
