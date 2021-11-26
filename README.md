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
                 [-ovd] [-oad] [-W] [-v] [-pa] [-S] [-V]
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
  -ovd, --output_volcano_data
                        Output volcano data (ID profile) for the selected
                        target volcano in a json-format file. NB. Verbose mode
                        needs to be activated to be able to use this feature.
  -oad, --output_analogues_data
                        Output volcano data (ID profile) for all the top
                        analogue volcanoes, for the selected target volcano
                        and weighting scheme, in a json-format file. NB.
                        Verbose mode needs to be activated to be able to use
                        this feature.
  -W, --website         Open GVP website for top analogue volcano
  -v, --verbose         Print debug-level logging output, ID profile for the
                        selected target volcano, and include single-criterion
                        analogy values, besides the total analogy values, in
                        the PyVOLCANS results.
  -pa, --plot_apriori   Generate bar plots displaying: (1) values of single-
                        criterion and total analogy between the target volcano
                        and any 'a priori' analogues chosen by the user; and
                        (2) percentages of 'better analogues' (for the target
                        volcano) than each of the 'a priori' analogues,
                        considering all volcanoes in the GVP database.
  -S, --save_figures    Save all generated figures
  -V, --version         Print PyVOLCANS package version and exit
```

Calling PyVOLCANS with a volcano name returns the top 10 analogue volcanoes:

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

In verbose mode (e.g. `$ pyvolcans Hekla --verbose`), PyVOLCANS provides further information regarding the weights selected for each volcanological criteria, as well as the values for each single-criterion analogy, which combined make up the `total_analogy` values (NB. The total analogy is a weighted average of the single-criterion analogies. Please see equation 1 in [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3) for more details).

As of [PyVOLCANS v1.3.0](https://github.com/BritishGeologicalSurvey/pyvolcans/releases/tag/v1.3.0), the verbose mode also provides the _ID profile_ (i.e. summary of volcanological data available for VOLCANS calculations) for the specific volcano of interest. Please see [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3) for further details on how these data are used to compute single-criterion and total-analogy values.

For example:

```
$ pyvolcans Hekla --verbose

PyVOLCANS: Supplied weights: {'tectonic_setting': 0.2, 'geochemistry': 0.2, 'morphology': 0.2, 'eruption_size': 0.2, 'eruption_style': 0.2}

Top 10 analogue volcanoes for Hekla, Iceland (372070):
              name       country  smithsonian_id  total_analogy  ATs        AG        AM       ASz       ASt
       Torfajokull       Iceland          372050       0.941676  0.2  0.188235  0.187584  0.180280  0.185577
       Bardarbunga       Iceland          373030       0.921407  0.2  0.188235  0.187584  0.172727  0.172861
      Prestahnukur       Iceland          371070       0.919877  0.2  0.188235  0.189474  0.169091  0.173077
        Langjokull       Iceland          371080       0.915929  0.2  0.188235  0.177193  0.169091  0.181410
           Hengill       Iceland          371050       0.911855  0.2  0.192157  0.173684  0.169091  0.176923
 Brennisteinsfjoll       Iceland          371040       0.907751  0.2  0.164706  0.184211  0.169091  0.189744
        Kverkfjoll       Iceland          373050       0.906833  0.2  0.188235  0.187584  0.169091  0.161923
       Fremrinamar       Iceland          373070       0.905074  0.2  0.188235  0.168421  0.169091  0.179327
           Ecuador       Ecuador          353011       0.901611  0.2  0.164706  0.194737  0.169091  0.173077
     Marion Island  South Africa          234070       0.892960  0.2  0.141176  0.200000  0.169091  0.182692

ID profile for Hekla, Iceland (372070):
{
  "name": "Hekla",
  "country": "Iceland",
  "smithsonian_id": 372070,
  "tectonic_setting": {
    "0.0": "Rift Oceanic Crust"
  },
  "geochemistry": {
    "Foidite": 0.0,
    "Phonolite": 0.0,
    "Trachyte": 0.0,
    "Trachyandesite/Basaltic trachyandesite": 0.0,
    "Phono-tephrite/Tephri-phonolite": 0.0,
    "Tephrite/Basanite/Trachybasalt": 0.0,
    "Basalt": 0.25,
    "Andesite": 0.25,
    "Dacite": 0.25,
    "Rhyolite": 0.25
  },
  "morphology": 0.39473684210526316,
  "eruption_size": {
    "VEI leq 2": 0.26666666666666666,
    "VEI 3": 0.35,
    "VEI 4": 0.2833333333333333,
    "VEI 5": 0.1,
    "VEI 6": 0.0,
    "VEI 7": 0.0,
    "VEI 8": 0.0
  },
  "eruption_style": {
    "Lava flow and/or fountaining": 0.8769230769230769,
    "Ballistics and tephra": 0.6923076923076923,
    "Phreatic and phreatomagmatic activity": 0.0,
    "Water-sediment flows": 0.15384615384615385,
    "Tsunamis": 0.015384615384615385,
    "Pyroclastic density currents": 0.09230769230769231,
    "Edifice collapse/destruction": 0.0,
    "Caldera formation": 0.0
  }
}
```

### Volcano naming conventions

Please note that some volcano names are composed of more than one word, such as Rincón de la Vieja (Costa Rica) or St. Helens (USA). In these cases, please wrap around the volcano name using quotation marks. For example:

```
$ pyvolcans "Rincon de la Vieja"

Top 10 analogue volcanoes for Rincon de la Vieja, Costa Rica (345020):
           name     country  smithsonian_id  total_analogy
    Sorikmarapi   Indonesia          261120       0.965415
         Zaozan       Japan          283190       0.963941
         Mahawu   Indonesia          266110       0.959122
 Akita-Yakeyama       Japan          283260       0.958577
         Lascar       Chile          355100       0.956498
     Miravalles  Costa Rica          345030       0.955624
     Hakkodasan       Japan          283280       0.955043
           Poas  Costa Rica          345040       0.954254
     Midagahara       Japan          283080       0.952637
       Maruyama       Japan          285061       0.951902
```

Please also note that some naming conventions used in the [Holocene Volcano List](https://volcano.si.edu/list_volcano_holocene.cfm) of the Global Volcanism Program (GVP) include the sorting of some words in the volcano name, separated by commas. For example: "Fournaise, Piton de la" (France), "Sawad, Harra Es-" (Yemen) or "Bravo, Cerro" (Colombia). One of the functionalities of PyVOLCANS is to provide a list of volcano-name suggestions, if the volcano name introduced by the user contains a typo and/or is arranged in a different word order. Please see the following command example:

```
$ pyvolcans "Nevados de Chillan"

PyVOLCANS: Nevados de Chillan not found! Did you mean:
                 name          country  smithsonian_id
  Chillan, Nevados de            Chile          357070
     Chachani, Nevado             Peru          354007
    Huila, Nevado del         Colombia          351050
      Casiri, Nevados             Peru          354060
    Cuernos de Negros      Philippines          272010
   Carrán-Los Venados            Chile          357140
      Chaine des Puys           France          210020
     Ruiz, Nevado del         Colombia          351020
             Red Hill    United States          327812
 Incahuasi, Nevado de  Chile-Argentina          355125
```

```
$ pyvolcans "Chillan, Nevados de"

Top 10 analogue volcanoes for Chillan, Nevados de, Chile (357070):
                name          country  smithsonian_id  total_analogy
          Guallatiri            Chile          355020       0.972271
 San Pedro-San Pablo            Chile          355070       0.970770
            San Jose  Chile-Argentina          357020       0.968865
             Galeras         Colombia          351080       0.966499
         Peuet Sague        Indonesia          261030       0.965005
         Zhupanovsky           Russia          300120       0.964308
             Bulusan      Philippines          273010       0.963809
          Chiginagak    United States          312110       0.963711
          Villarrica            Chile          357120       0.961412
            Cotopaxi          Ecuador          352050       0.960387
```

Finally, please be aware of possible synonyms and subfeatures of the volcanic systems listed in the [Holocene Volcano List](https://volcano.si.edu/list_volcano_holocene.cfm) of GVP. For example, "[Fagradalsfjall](https://volcano.si.edu/volcano.cfm?vn=371030&vtab=Subfeatures)" for "[Krýsuvík-Trölladyngja](https://volcano.si.edu/volcano.cfm?vn=371030&vtab=GeneralInfo)" (Iceland) or "[Sakurajima](https://volcano.si.edu/volcano.cfm?vn=282080&vtab=Subfeatures)" for "[Aira](https://volcano.si.edu/volcano.cfm?vn=282080&vtab=GeneralInfo)" (Japan). In these situations, we recommend PyVOLCANS users perform a simple Google Search using: "Fagradalsfjall GVP" or "Sakurajima GVP". In general, the first search result should point to the GVP website of the volcanic system of interest. Users can then use that volcano name to run their volcano analogues searches via `pyvolcans`.

For a comprehensive description of the purpose, input arguments and output variables for each of the functions and methods used by `pyvolcans`, please follow the link to the [source scripts](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/main/pyvolcans).

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
