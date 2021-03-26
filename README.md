# Open-access VOLCANS

Collaborative effort to create an free-software (Python), open-access version of VOLCANS (https://doi.org/10.1007/s00445-019-1336-3). 1st stage: provide the users with results from VOLCANS. 2nd stage: clean, re-test and open the whole VOLCANS code

## Installation

`pyvolcans` can be imported to a new environment as follows:

```
pip install git+https://github.com/BritishGeologicalSurvey/pyvolcans.git
```

It is necessary to have git installed and on the system path.

This method adds `pyvolcans` to the virtual environment PATH so that it can be
used from any directory.

## How to use

### Basic example of usage
Calling PyVOLCANS with a volcano name returns the 10 top analogue volcanoes:
```
$ pyvolcans Hekla

              name       country  smithsonian_id  total_analogy
       Torfajokull       Iceland          372050       0.941676
       Bardarbunga       Iceland          373030       0.921407
      Prestahnukur       Iceland          371070       0.919877
        Langjokull       Iceland          371080       0.915929
           Hengill       Iceland          371050       0.911855
 Brennisteinsfjoll       Iceland          371040       0.907751
        Kverkfjoll       Iceland          373050       0.906833
       Fremrinamar       Iceland          373070       0.905074
           Ecuador       Ecuador          353011       0.901611
     Marion Island  South Africa          234070       0.892960
```
Calling PyVOLCANS help gives details of command line options:
```
$ pyvolcans --help

usage: pyvolcans [-h] [--apriori [APRIORI [APRIORI ...]]]
                 [-Ts TECTONIC_SETTING] [-G ROCK_GEOCHEMISTRY] [-M MORPHOLOGY]
                 [-Sz ERUPTION_SIZE] [-St ERUPTION_STYLE] [--count COUNT] [-w]
                 [-W] [-v] [-V]
                 volcano

positional arguments:
  volcano               Set target volcano name or Smithsonian ID

optional arguments:
  -h, --help            show this help message and exit
  --apriori [APRIORI [APRIORI ...]]
                        Provide one or more a priori analogue volcanoes
  -Ts TECTONIC_SETTING, --tectonic_setting TECTONIC_SETTING
                        Set tectonic setting weight (e.g. '0.2' or '1/5')
  -G ROCK_GEOCHEMISTRY, --rock_geochemistry ROCK_GEOCHEMISTRY
                        Set rock geochemistry weight (e.g. '0.2' or '1/5')
  -M MORPHOLOGY, --morphology MORPHOLOGY
                        Set volcano morphology weight (e.g. '0.2' or '1/5')
  -Sz ERUPTION_SIZE, --eruption_size ERUPTION_SIZE
                        Set eruption size weight (e.g. '0.2' or '1/5')
  -St ERUPTION_STYLE, --eruption_style ERUPTION_STYLE
                        Set eruption style weight (e.g. '0.2' or '1/5')
  --count COUNT         Set the number of top analogue volcanoes
  -w, --write_csv_file  Write list of top analogue volcanoes as .csv file
  -W, --website         Open GVP website for top analogue volcano
  -v, --verbose         Print debug-level logging output
  -V, --version         Show package version
```

### More complex example 1

### More complex example 2

### More complex example 3


## For developers

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
