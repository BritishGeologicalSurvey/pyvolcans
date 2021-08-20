# VOLCANS: code numbering

This README file details the code numbering adopted in the different csv files inside the folder:
[../../VOLCANS_csv_files](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/matlab-scripts/pyvolcans/VOLCANS_csv_files).
This numbering was adopted to ease the calculations performed by the Matlab scripts that compose the VOLCANS method.

Please note that, in some cases, the code numbering can be directly checked on `.xls` files located inside
the [current folder](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers) (please see descriptions below). When this is not available, a legend is provided in this file, showing the correspondence between categorical variables and code numbering (please see next sub-sections).

Please also note that the `NO DATA` value used across all data files is `-9999`.

## VOTW467_8May18_volcano_data.csv

Code numbering for all the categorical variables can be found in the file [VOTW467_8May18_Holocene_list_textdata_portable.xls](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers/VOTW467_8May18_Holocene_list_textdata_portable.xls)
(the variable displaying the code number in the spreadsheet is given between brackets):

Country (country#), Region (reg#), Subregion (subreg#), Primary Volcano Type (volctype#), Activity Evidence (procdate1),
Dominant Rock Type (domrock#), Tectonic Setting (tectset#).

Please also note the following four aspects:

1. The variable ''Volcano Number'' (also expressed as ''VNUM'' in other data files) denotes a unique volcano identifier that
the GVP database assigns to each volcanic system listed in the database.

2. The variables ''Major Rock 1-5'' and ''Minor Rock 1-5'' use the same code numbering as the variable ''Dominant Rock Type''.

3. The variable ''Last Known Eruption'' is given in years from current era, with negative values expressing dates before
current era (BCE). The same convention is applicable to variables ''Start Year'' in file [VOTW467_8May18_eruption_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_eruption_data.csv),
''Eruption Start Year'' in file [VOTW467_8May18_event_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_event_data.csv), and ''Date of completeness'' in [MeadMagill2014_June2018.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/MeadMagill2014_June2018.csv).

4. The variables ''Latitude'' and ''Longitude'' (also included in the file [VOTW467_8May18_Eruption_list_textdata_portable.xls](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers/VOTW467_8May18_Eruption_list_textdata_portable.xls))
correspond to the approximate spatial location of the volcanic system, and are expressed in decimal degrees.

## VOTW467_8May18_eruption_data.csv

Code numbering for the categorical variable ''VEI Modifier'' can be found in the file [VOTW467_8May18_Eruption_list_textdata_portable.xls](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers/VOTW467_8May18_Eruption_list_textdata_portable.xls)
(please see column ''VEImod#'').

For the variable ''Eruption Category'', the following code numbering is applied:

1 = Confirmed Eruption

3 = Uncertain Eruption 

## VOTW467_8May18_event_data.csv

Code numbering for the categorical variable ''Event Type'' can be found in the file [VOTW467_8May18_Event_list_textdata_portable.xls](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers/VOTW467_8May18_Event_list_textdata_portable.xls)
(please see column ''event#'').

For the variable ''group#'', the following code numbering is applied (please also see [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)):

1 = Lava flow and/or fountaining

2 = Ballistics and Tephra

3 = Phreatic and phreatomagmatic activity 

4 = Water-sediment flows

5 = Tsunamis

6 = Pyroclastic density currents

7 = Edifice collapse/destruction

8 = Caldera formation

## MeadMagill2014_June2018.csv

Code numbering for the categorical variable ''Region/Country code'' corresponds with the values in column ''Name''.
These values are the same as those found in file [VOTW467_8May18_Holocene_list_textdata_portable.xls](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers/VOTW467_8May18_Holocene_list_textdata_portable.xls), for variables
''Region (reg#)'' and ''Country (country#)''. The variable ''Region/Country'' denotes whether a given entry corresponds
with a region (0) or a country (1).

## PC81_GR2014_data.csv

The following legend and code numbering is applicable to the merged database of volcano morphology:

- `VNUM`: Volcano Number (i.e. GVP unique volcano identifier)

- `Sub-feature`: The entry corresponds with a sub-feature (1) of a unique VNUM entry in GVP v4.6.7, or does not (0). In the latter case, the entry represents the _main_ volcanic feature of the corresponding VNUM.

- `small crater?`: The entry is (1) or is not (0) associated with a ''small crater'' flag according to the [Grosse et al. (2014)](https://doi.org/10.1007/s00445-013-0784-4) database.

- `NB`: It indicates whether there are any relevant remarks about the calculation of the morphology features displayed in the entry (these remarks coming from [Pike and Clow (1981)](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume), hereinafter PC81, and [Grosse et al. (2014)](https://doi.org/10.1007/s00445-013-0784-4), hereinafter GR2014):
    
    * 1	= One or more dimensions uncertain and subject to revision.
    * 2 = Height and width calculated from volumetric information only.
    * 3 = Estimate of lake depth included in total crater depth.
    * 4 = Island volcano: height and width down to sea level only.
    * 5 = Height and width down to sea level only, plus one or more dimensions uncertain and subject to revision.

- `W*_T from`: It indicates from which database the value of `W*` (volcano's edifice half-width, please see below) was taken from:

    * `W*_T from` = 0 &rarr; [PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume) database.
    * `W*_T from` = 1 &rarr; [GR2014](https://doi.org/10.1007/s00445-013-0784-4) database.

- `d`: Average diameter of crater rim-crest ([PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume)) or ''Crater Width'' variable in [GR2014](https://doi.org/10.1007/s00445-013-0784-4).

- `h`: Average depth of crater floor below rim crest ([PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume)) or ''Crater Depth'' variable in [GR2014](https://doi.org/10.1007/s00445-013-0784-4).

- `H`: Average height of rim crest above pre-volcano topographic datum ([PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume)) or ''Height Max'' variable in [GR2014](https://doi.org/10.1007/s00445-013-0784-4).

- `W*`:	W\* = W + (1/2 · d) in [PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume), where W denotes the average half-width of the volcano, i.e. flank rim crest to edge of edifice; or W\* = 1/2 · W<sub>basal</sub> in [GR2014](https://doi.org/10.1007/s00445-013-0784-4), where W<sub>basal</sub> denotes the ''Basal Width'' variable.

- `C`: Circularity of rim crest, i.e. area inscribed circle/area circumscribed circle (only available in [PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume)).

- `ave. ei`: Ellipticity index [average contours] variable in [GR2014](https://doi.org/10.1007/s00445-013-0784-4).

- `T`: T = d/(2W + d) if taken from [PC81](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume); or T = W<sub>summit</sub>/W<sub>basal</sub> (''Summit Width/Basal Width'' variable) if taken from [GR2014](https://doi.org/10.1007/s00445-013-0784-4).

- `sv`: Secondary vents, i.e. ''Sec. Peaks [total]'' variable in [GR2014](https://doi.org/10.1007/s00445-013-0784-4).
