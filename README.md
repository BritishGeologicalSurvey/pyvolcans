# PyVOLCANS

> PyVOLCANS: A Python package to flexibly explore similarities and differences between volcanic systems

The main goal of PyVOLCANS is to help alleviate data-scarcity issues in volcanology, and contribute to developments in a range of topics, including (but not limited to): quantitative volcanic hazard assessment at local to global scales, investigation of magmatic and volcanic processes, and even teaching and scientific outreach. We hope that future users of PyVOLCANS will include any volcano scientist or enthusiast with an interest in exploring the similarities and differences between volcanic systems worldwide. Please visit our [wiki pages](https://github.com/BritishGeologicalSurvey/pyvolcans/wiki) for more information.

## Installation instructions

PyVOLCANS can be installed from PyPI as follows:

```
pip install pyvolcans
```

This method adds `pyvolcans` to the virtual environment PATH so that it can be
used from any directory.


## API documentation and example usage

Users interact with PyVOLCANS via the command-line tool. The `--help` command describes the possible options.

```
$ pyvolcans --help

usage: pyvolcans [-h] [--apriori [APRIORI [APRIORI ...]]]
                 [-Ts TECTONIC_SETTING] [-G ROCK_GEOCHEMISTRY] [-M MORPHOLOGY]
                 [-Sz ERUPTION_SIZE] [-St ERUPTION_STYLE] [--count COUNT] [-w]
                 [-W] [-v] [-pa] [-S] [-V]
                 volcano

positional arguments:
  volcano               Set target volcano name or Smithsonian ID (VNUM)

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
  -v, --verbose         Print debug-level logging output, and include single-
                        criterion analogy values, besides the total analogy
                        values, in the PyVOLCANS results
  -pa, --plot_apriori   Generate bar plots displaying the values of single-
                        criterion and total analogy between the target volcano
                        and any 'a priori' analogues chosen by the user.
  -S, --save_figures    Save all generated figures
  -V, --version         Print PyVOLCANS package version and exit
```

Calling PyVOLCANS with a volcano name returns the 10 top analogue volcanoes:

```
$ pyvolcans Hekla

Top 10 analogue volcanoes for Hekla, Iceland (372070):
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

A comprehensive description of the purpose, input arguments and output variables for each of the functions and methods used by `pyvolcans` can be found in the [source scripts](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/main/pyvolcans).

Please also visit our [wiki pages](https://github.com/BritishGeologicalSurvey/pyvolcans/wiki) to find out more details on the usage of PyVOLCANS, as well as several example outputs for different commands.


## Community

### For users

The best way to get in touch to ask questions, submit bug reports or contribute code is by submitting an [issue](https://github.com/BritishGeologicalSurvey/pyvolcans/issues) in this repository.

### For developers

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

### Maintainers

`PyVOLCANS` was created by and is maintained by British Geological Survey
Volcanology and Digital Capabilities.

+ Pablo Tierz ([PTierz](https://github.com/PTierz))
+ Vyron Christodoulou ([mobiuscreek](https://github.com/mobiuscreek))
+ John A Stevenson ([volcan01010](https://github.com/volcan01010))

## Licence

`PyVOLCANS` and the associated `VOLCANS` Matlab scripts are distributed under the [LGPL v3.0 licence](LICENSE).
Copyright: © BGS / UKRI 2021
