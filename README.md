# PyVOLCANS

An open-access Python tool that generates data-driven sets of analogue
volcanoes for any Holocene volcano listed in the Global Volcanism Program (GVP)
Volcanoes Of The World database (v. 4.6.7), based on the VOLCANS (VOLCano
ANalogues Search) method presented by Tierz, Loughlin and Calder (2019):
[https://doi.org/10.1007/s00445-019-1336-3](https://doi.org/10.1007/s00445-019-1336-3)

VOLCANS uses five volcanological criteria (tectonic setting, rock geochemistry,
volcano morphology, eruption size and eruption style), and a structured
combination of them, to quantify overall multi-criteria (or total) volcano
analogy among any two volcanoes in the GVP database. The data used by the
method are extracted from the GVP database as well as from a merged database of
volcano morphology (after Pike and Clow, 1981; Grosse et al., 2014).

PyVOLCANS provides its user with full flexibility to identify customised sets
of analogue volcanoes, by exploring three main variables:

        (1) target volcano (or volcano of interest);
        (2) weighting scheme (i.e. set of weights given to each of the five
        volcanological criteria to calculate multi-criteria, total analogy);
        (3) number of 'top' analogue volcanoes (i.e. those with the highest
        value of analogy with the target volcano).

In addition, PyVOLCANS allows the user to compare the values of total analogy
computed for 'a priori analogues' (i.e. volcanoes thought to be good analogues
to the target volcano by other strands of evidence, e.g. expert knowledge) with
those computed for the rest of volcanoes in the GVP database. This permits
investigation of sets of analogue volcanoes for varied purposes, and makes
PyVOLCANS a useful complementary method to expert-derived analogue volcanoes.
Please see [Tierz et al. (2019)](https://doi.org/10.1007/s00445-019-1336-3) for
more details on the VOLCANS method.

## Installation

PyVOLCANS can be imported to a new environment as follows:

```
pip install pyvolcans
```

It is necessary to have Git installed and on the system path.

This method adds `pyvolcans` to the virtual environment PATH so that it can be
used from any directory.


## How to use PyVOLCANS

Calling PyVOLCANS help gives details of command line options:

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
that PyVOLCANS assigns to each of the volcanological criteria: tectonic
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

NB. You can also use fractions to define the weighting scheme. For instance,
the last command above is equivalent to: `$ pyvolcans Hekla -Sz 1/2 -St 1/2`

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
```

Or save your PyVOLCANS results into a comma-separated-value (csv) file that
you might use for your records and/or to perform further analyses on the data.

For example, typing:

```
$ pyvolcans Hekla --write_csv
```

generates the same standard PyVOLCANS output as `$ pyvolcans Hekla`, but,
in addition, it saves a file named:

`Hekla_top10analogues_Ts0200G0200M0200Sz0200St0200.csv`

into the current working directory.

The filename is a unique identifier of the three main parameters that are used
by PyVOLCANS, each separated by the underscore sign:

    (1) target volcano (`Hekla`);
    (2) weighting scheme (`Ts0200G0200M0200Sz0200St0200`)
    (3) number of top analogue volcanoes (`top10analogues`)

The weight selected for each volcanological criterion is indicated by the
abbreviation of the criterion (see above and in Equation 1 of Tierz et al.,
2019), followed by a four-digits number, where the first number indicates the
units value (either 0 or 1), and the following three numbers indicate the
decimals of the weight value. Thus, the following examples apply:

`0200` denotes `0.200`, `0850` denotes `0.850`,
`0125` denotes `0.125`, `1000` denotes `1.000`, etc.

The content of the csv file is the same as the standard PyVOLCANS output:

```
$ cat Hekla_top10analogues_Ts0200G0200M0200Sz0200St0200.csv

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

PyVOLCANS can also be used to investigate sets of analogue volcanoes that have
been derived using other approaches different from PyVOLCANS, e.g. analogue
volcanoes based on expert knowledge. Such analogue volcanoes might be called
'a priori analogues' ([Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)).
PyVOLCANS offers the user the possibility of checking for the proportion (or
percentage) of Holocene volcanoes in the GVP database that are 'better
analogues' (i.e. have a higher value of total analogy with the target volcano),
compared to each of the a priori analogues provided by the user.

For example, if we choose Volcán de Fuego (Guatemala) and the following
a priori analogues (please see Figure 6 in
[Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)): Villarrica,
Llaima (Chile), Pacaya (Guatemala), Reventador, Tungurahua (Ecuador).

```
$ pyvolcans Fuego --apriori Villarrica Llaima Pacaya Reventador Tungurahua

Top 10 analogue volcanoes for Fuego, Guatemala (342090):
         name           country  smithsonian_id  total_analogy
 Klyuchevskoy            Russia          300260       0.970910
       Semeru         Indonesia          263300       0.963634
       Osorno             Chile          358010       0.955407
      Merbabu         Indonesia          263240       0.953673
       Tacana  Mexico-Guatemala          341130       0.951295
  Chikurachki            Russia          290360       0.951209
       Pavlof     United States          312030       0.950073
        Baker     United States          321010       0.949815
   Acatenango         Guatemala          342080       0.949274
   Shishaldin     United States          311360       0.948061


According to PyVOLCANS, the following percentage of volcanoes in the GVP database
are better analogues to Fuego than the 'a priori' analogues reported below:

Villarrica (357120): 2%

Llaima (357110): 2%

Pacaya (342110): 8%

Reventador (352010): 7%

Tungurahua (352080): 7%
```

Please note that: (1) the percentages are calculated to the closest unit
percentage, and (2) given the total number of Holocene volcanoes in the GVP
database v.4.6.7 used by PyVOLCANS (N = 1439), 1% corresponds to 14 volcanoes,
approximately.

It is also critical to be aware that any value of total analogy calculated by
PyVOLCANS, and therefore any percentage of 'better analogues', is not only
dependent on the choice of target volcano and a priori analogues, but also,
importantly, on the specific choice of weighting scheme used for each run of
PyVOLCANS. Different weighting schemes may lead to different sets of top
analogue volcanoes as well as to different percentages of 'better analogues'
for any pair of target volcano-a priori analogue.

Hence, using the equal-weight scheme for eruption size and style mentioned
above (scheme B in [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3))
does modify the PyVOLCANS results in the example for Volcán de Fuego:

```
$ pyvolcans Fuego -Sz 1/2 -St 1/2 --apriori Villarrica Llaima Pacaya Reventador Tungurahua

Top 10 analogue volcanoes for Fuego, Guatemala (342090):
         name        country  smithsonian_id  total_analogy
    Momotombo      Nicaragua          344090       0.985340
        Pagan  United States          284170       0.982429
       Pavlof  United States          312030       0.982149
 Klyuchevskoy         Russia          300260       0.981609
  Karangetang      Indonesia          267020       0.977516
   Villarrica          Chile          357120       0.977199
       Semeru      Indonesia          263300       0.976578
     Lewotobi      Indonesia          264180       0.976012
     Karymsky         Russia          300130       0.975861
       Ambrym        Vanuatu          257040       0.974410


According to PyVOLCANS, the following percentage of volcanoes in the GVP database
are better analogues to Fuego than the 'a priori' analogues reported below:

Villarrica (357120): 1%

Llaima (357110): 2%

Pacaya (342110): 2%

Reventador (352010): 7%

Tungurahua (352080): 26%
```

WARNING! Please note that, in the current version of PyVOLCANS, defining the
set of a priori analogues as a mix of data types (e.g. str for volcano names
and int for volcano number, VNUM (or Smithsonian ID)) does not provide the user
with the expected data for the percentages of better analogues.

PLEASE USE either a set of volcano names or a set of volcano numbers to define
your set of a priori analogues when running PyVOLCANS. Many thanks.

#### Plotting capabilities

From release `v1.1.0` onwards, users can also visualise: (1) the single-criterion
and total (multi-criteria) analogy values between the target volcano and any _a priori_
analogue volcano selected by the user, and (2) the percentage of _better analogues_
(than each of the _a priori_ analogues) available in the whole GVP database, for the
specific target volcano chosen.

These results are provided as bar plots when the user selects the optional flag
`--plot_apriori` (or `-pa`):

```
$ pyvolcans Fuego --apriori Villarrica Llaima Pacaya Reventador Tungurahua --plot_apriori
```

If the user wants to save the generated figures (.png format, 600 dpi resolution),
the optional flag `--save_figures` (or `-S`) should be selected, together with the
`--plot_apriori` (or `-pa`) flag.


## Analogy matrices

In the original VOLCANS paper, the analogy matrices were calculated in Matlab.
Please note that these matrices are based on data contained in the Volcanoes
of the World database (GVP) v. 4.6.7 (Tierz et al., 2019).

Please also note that a few minor modifications have been implemented on some
of the matrices, as a result of research developed since the original VOLCANS
paper was published. These changes are the following:

- Sinabung, Indonesia (261080): (1) lava flows and lahars from the 2013–2018
eruption are included; and (2) the 2013–2018 eruption is updated to VEI 4
(GVP, 2013, database version 4.7.4). Please see [Tierz et al. (2019)](https://doi.org/10.1007/s00445-019-1336-3).

- Alutu, Ethiopia (221270): rock type 'Dacite' is removed from the GVP profile
of Aluto volcano. Please see [Tierz et al. (2020)](https://doi.org/10.1029/2020GC009219).

- Quetrupillán, Chile (357121): the following rock types are used instead of
those in the GVP 4.6.7 profile: Major (Trachyte), Minor (Basalt, Basaltic
andesite, Rhyolite). A crater diameter of 1.37 km (equivalent to the value
of summit width in [Grosse et al., 2014](https://doi.org/10.1007/s00445-013-0784-4))
is used for Quetrupillán. Please see [Simmons et al. (2020)](https://doi.org/10.30909/vol.03.01.115137)
and Simmons (2020) [_The Quetrupillán Volcanic Complex, Chile:
Holocene volcanism, magmatic plumbing system, and future hazards_, PhD Thesis,
University of Edinburgh].

The initial releases of PyVOLCANS make use these pre-calculated analogy
matrices. This was the quickest way of making VOLCANS results available
to users. In a future release, we aim to include a Python version of the
code that calculates the analogies based on volcano characterisics.
This will make the method more transparent.

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
pytest -v test
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
