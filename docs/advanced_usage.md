# Advanced Usage

## Modifying the weighting scheme and number of top analogue volcanoes

Use the optional flags -Ts, -G, -M, -Sz, -St to customise the weights that PyVOLCANS assigns to each of the volcanological criteria: tectonic setting, rock geochemistry, volcano morphology, eruption size (Volcanic Explosivity Index, VEI, [Newhall and Self, 1982](https://doi.org/10.1029/JC087iC02p01231)), and eruption style, respectively (abbreviations are as in [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3), Equation 1).

For example, call PyVOLCANS using an equal-weight scheme between eruption size and eruption style, setting the other volcanological criteria to 0 (Scheme B in [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)):

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

NB. You can also use fractions to define the weighting scheme. For instance, the last command above is equivalent to: `$ pyvolcans Hekla -Sz 1/2 -St 1/2`

## Modifying the number of top analogues

Use the optional flag --count to change the number of top analogue volcanoes:

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

## Getting verbose output

Use the optional flag --verbose to print the weighting scheme on-screen, and also to obtain the single-criterion analogy values, in addition to the total analogy values that PyVOLCANS outputs by default:

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

## Saving to CSV

You can save your PyVOLCANS results into a comma-separated-value (csv) file that you might use for your records and/or to perform further analyses on the data.

For example, typing:

`$ pyvolcans Hekla --write_csv`

generates the same standard PyVOLCANS output as `$ pyvolcans Hekla`, but, in addition, it saves a file named:

`Hekla_top10analogues_Ts0200G0200M0200Sz0200St0200.csv`

into the current working directory.

The filename is a unique identifier of the three main parameters that are used by PyVOLCANS, each separated by the underscore sign:

(1) target volcano (`Hekla`);
(2) weighting scheme (`Ts0200G0200M0200Sz0200St0200`)
(3) number of top analogue volcanoes (`top10analogues`)
The weight selected for each volcanological criterion is indicated by the abbreviation of the criterion (see above and in Equation 1 of [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)), followed by a four-digits number, where the first number indicates the units value (either 0 or 1), and the following three numbers indicate the decimals of the weight value. Thus, the following examples apply:

0200 denotes 0.200, 0850 denotes 0.850, 0125 denotes 0.125, 1000 denotes 1.000, etc.

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

## Investigating _a priori_ analogue volcanoes

PyVOLCANS can also be used to investigate sets of analogue volcanoes that have been derived using other approaches different from PyVOLCANS, e.g. analogue volcanoes based on expert knowledge. Such analogue volcanoes might be called 'a priori analogues' ([Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)). PyVOLCANS offers the user the possibility of checking for the proportion (or percentage) of Holocene volcanoes in the GVP database that are 'better analogues' (i.e. have a higher value of total analogy with the target volcano), compared to each of the a priori analogues provided by the user.

For example, if we choose Volcán de Fuego (Guatemala) and the following a priori analogues (please see Figure 6 in [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)): Villarrica, Llaima (Chile), Pacaya (Guatemala), Reventador, Tungurahua (Ecuador), the results are the following:

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

Please note that: (1) the percentages are calculated to the closest unit percentage, and (2) given the total number of Holocene volcanoes in the GVP database v.4.6.7 used by PyVOLCANS (N = 1439), 1% corresponds to 14 volcanoes, approximately.

## Dependence of _better analogues_ on the weighting scheme

It is also critical to be aware that any value of total analogy calculated by PyVOLCANS, and therefore any percentage of 'better analogues', is not only dependent on the choice of target volcano and a priori analogues, but also, importantly, on the specific choice of weighting scheme used for each run of PyVOLCANS. Different weighting schemes may lead to different sets of top analogue volcanoes as well as to different percentages of 'better analogues' for any pair of target volcano-a priori analogue.

Hence, using the equal-weight scheme for eruption size and style mentioned above (scheme B in [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)) does modify the PyVOLCANS results in the example for Volcán de Fuego:

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

WARNING! Please note that, in the current version of PyVOLCANS, defining the set of a priori analogues as a mix of data types (e.g. str for volcano names and int for volcano number, VNUM (or Smithsonian ID)) does not provide the user with the expected data for the percentages of better analogues.

PLEASE USE either a set of volcano names or a set of volcano numbers to define your set of a priori analogues when running PyVOLCANS. Many thanks.

## Plotting capabilities

From release [v1.1.0](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/v1.1.0) onwards, users can also visualise: (1) the single-criterion
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
