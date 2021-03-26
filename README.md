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

## How to use PyVOLCANS

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

### Default call to PyVOLCANS

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

NB. The default weighting scheme used by PyVOLCANS is an equal-weight of all
    volcanological criteria (Scheme A in Tierz et al., 2019).

### Modifying the weighting scheme and number of top analogue volcanoes

Use the optional flags `-Ts`, `-G`, `-M`, `-Sz`, `-St` to customise the weights
that PyVOLCANS assigns to each of the volcanological criterion: tectonic
setting, rock geochemistry, volcano morphology, eruption size (Volcanic
Explosivity Index, VEI, Newhall and Self, 1982), and eruption style,
respectively (abbreviations are as in Tierz et al., 2019, Equation 1).

For example, call PyVOLCANS using an equal-weight scheme between eruption size
and eruption style, setting the other volcanological criteria to 0 (Scheme B in
Tierz et al., 2019):

```
$ pyvolcans Hekla -Sz 0.5 -St 0.5

Top 10 analogue volcanoes for Hekla, Iceland (372070):
               name        country  smithsonian_id  total_analogy
              Taupo    New Zealand          241070       0.947620
         Kikhpinych         Russia          300180       0.940538
      Chichinautzin         Mexico          341080       0.934044
 Carrán-Los Venados          Chile          357140       0.933013
           Newberry  United States          322110       0.930016
           Khodutka         Russia          300053       0.927797
 Tangkoko-Duasudara      Indonesia          266130       0.922440
             Dukono      Indonesia          268010       0.921541
              Okmok  United States          311290       0.921246
        Agua de Pau       Portugal          382090       0.921154
```

NB. You can use fractions to define the weighting scheme.
For instance: `$ pyvolcans Hekla -Sz 1/2 -St 1/2`

Use the optional flag `--count` to change the number of top analogue volcanoes:

```
$ pyvolcans Hekla --count 5

Top 5 analogue volcanoes for Hekla, Iceland (372070):
         name  country  smithsonian_id  total_analogy
  Torfajokull  Iceland          372050       0.941676
  Bardarbunga  Iceland          373030       0.921407
 Prestahnukur  Iceland          371070       0.919877
   Langjokull  Iceland          371080       0.915929
      Hengill  Iceland          371050       0.911855

```

### Exploring other functionalities of PyVOLCANS

Use the optional flag `--verbose` to print the weighting scheme on-screen, and
also to obtain the single-criterion analogy values, in addition to the total
analogy values that PyVOLCANS outputs by default:

```
$ pyvolcans Hekla --verbose

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

```

Or save your PyVOLCANS results into a comma-separated-value (csv) file for your
record and/or to perform further analyses on the data:

For example, typing: `$ pyvolcans Hekla --write_csv`, generates the same
standard PyVOLCANS output as `$ pyvolcans Hekla`, but, in addition, it saves
a file named: `Hekla_top10analogues_Ts0200G0200M0200Sz0200St0200.csv`, into
the current working directory.

The filename is a unique identifier of the three main parameters that are used
by PyVOLCANS, separated by the underscored sign:

    (1) target volcano (`Hekla`);
    (2) weighting scheme (`Ts0200G0200M0200Sz0200St0200`)
    (3) number of top analogue volcanoes (`top10analogues`)

The weight selected for each volcanological criterion is indicated by the
abbreviation of the criterion (see above and in Equation 1 of Tierz et al.,
2019), followed by a four-digits number, where the first number indicates the
units value (either 0 or 1), and the following three numbers indicate the
decimals of the weight value. Thus, the following examples apply:

`0200` denotes `0.200`, `0850` denotes `0.85`,
`0125` denotes `0.125`, `1000` denotes `1.000`, etc.

The content of the csv file is very similar to the standard PyVOLCANS output:

```
$ head -n 11 Hekla_top10analogues_Ts0200G0200M0200Sz0200St0200.csv
name,country,smithsonian_id,total_analogy
Torfajokull,Iceland,372050,0.94168
Bardarbunga,Iceland,373030,0.92141
Prestahnukur,Iceland,371070,0.91988
Langjokull,Iceland,371080,0.91593
Hengill,Iceland,371050,0.91186
Brennisteinsfjoll,Iceland,371040,0.90775
Kverkfjoll,Iceland,373050,0.90683
Fremrinamar,Iceland,373070,0.90507
Ecuador,Ecuador,353011,0.90161
Marion Island,South Africa,234070,0.89296
```

### EXAMPLE OF A PRIORI ANALOGUES?

## Development

### For developers

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

### Maintainers

`PyVOLCANS` was created by and is maintained by British Geological Survey
Volcanology and Digital Capabilities.

+ Pablo Tierz ([PTierz](https://github.com/PTierz))
+ Vyron Christodoulou ([mobiuscreek](https://github.com/mobiuscreek))
+ John A Stevenson ([volcan01010](https://github.com/volcan01010))

### Licence

`PyVOLCANS` is distributed under the [LGPL v3.0 licence](LICENSE).
Copyright: © BGS / UKRI 2021
