# VOLCano ANalogues Search (VOLCANS)

This is a README file that describes the structure and content of the Matlab scripts (Mathworks, 2012) that integrate
the VOLCANS method presented by [Tierz, Loughlin and Calder (2019)](https://doi.org/10.1007/s00445-019-1336-3).

This set of scripts was used to derive all the [analogy matrices](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/main/pyvolcans/VOLCANS_mat_files/analogy_mats)
used by `PyVOLCANS`.

Please note that the VOLCANS Matlab code is provided _as-is_: in other words, without any cleaning for public use.
The eventual aim of us, creators of `PyVOLCANS` ([@PTierz](https://github.com/PTierz), [@mobiuscreek](https://github.com/mobiuscreek),
[@volcan01010](https://github.com/volcan01010)), is to port the entire Matlab code into Python, including it as part of future releases
of the `PyVOLCANS` code.

In the following, we provide: (1) a brief summary of the general process developed to generate the analogy matrices (for more details,
please see [Tierz et al., 2019](https://doi.org/10.1007/s00445-019-1336-3)); (2) overall descriptions of the main purpose of each of the
Matlab (`.m`) files available in the [current folder](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts); and (3) overall descriptions of the data contained in each of the csv files available
in folder [../VOLCANS_csv_files](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/matlab-scripts/pyvolcans/VOLCANS_csv_files). Detailed specifications of the numbering adopted for categorical variables, as well as the units
in which numerical variables are displayed (unless this is described in the header row of the csv files) are provided in
[../VOLCANS_csv_files/VOLCANS_code_numbers](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOLCANS_code_numbers).


## Volcano analogy

VOLCANS interprets volcano analogy as a quantitative measure of the similarity between any two volcanic systems listed in the Holocene
[Volcanoes Of The World database](https://volcano.si.edu/list_volcano_holocene.cfm) (v. 4.6.7), hosted by the Global Volcanism Program
(GVP) of the Smithsonian Institution. A volcano analogy of 0 denotes _no analogy_ between the two volcanoes, while a volcano analogy of
1 implies that the volcanoes are _perfect analogues_, considering the data available.

Five different volcanological criteria are considered in VOLCANS: tectonic setting, rock geochemistry, volcano morphology, eruption size
and eruption style. Volcano analogies based on only one criterion are termed: ''single-criterion analogies''. Volcano analogies based on
a structured combination (a weighted average) of two or more volcanological criteria are termed: ''multi-criteria or total analogies''.
Provided that each single-criterion analogy is a number between 0-1, and that the sum of weights defining the weighted average is equal
to 1, then each multi-criteria, or total analogy, is also a number between 0-1 (please see [Methods](https://link.springer.com/article/10.1007/s00445-019-1336-3#Sec6)
in Tierz et al., 2019, for more details). Please note that if there is no data available for a given volcano and a particular volcanological
criterion, then the corresponding single-criterion analogy values between that volcano and any other volcano in the GVP database are set to 0.

VOLCANS uses distance metrics to calculate each set of single-criterion analogies between any two volcanic systems in the GVP database.
These distance metrics are either based on: (a) linear distances between volcano-specific values, when the criterion is described by a
variable with single values for each volcano (tectonic setting, volcano morphology); (b) areal differences between volcano-specific Empirical
Cumulative Distribution Functions (ECDFs), when the criterion is described by a variable with a probability distribution (or histogram) for
each volcano (rock geochemistry, eruption size); or (c) normalised sum of differences between the frequency of occurrence of different groups
of hazardous events during eruptions at a given volcano (eruption style). Please see [Methods](https://link.springer.com/article/10.1007/s00445-019-1336-3#Sec6)
and [Table 2](https://link.springer.com/article/10.1007/s00445-019-1336-3/tables/2) in Tierz et al. (2019) for more details.

## Matlab scripts

The following [Matlab scripts](https://github.com/BritishGeologicalSurvey/pyvolcans/tree/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts) have the purpose of calculating volcano analogy matrices that contain the single-criterion volcano analogy values
for each of the possible combinations of two volcanoes in the GVP database. All the analogy matrices are N x N, where N (= 1439) is the total number of
volcanic systems listed in the GVP v4.6.7 database used in [Tierz et al. (2019)](https://doi.org/10.1007/s00445-019-1336-3).
Please also note that any single-criterion analogy between volcanoes X and Y, e.g. rock geochemistry (AG<sub>XY</sub>), is symmetric.
That is: AG<sub>XY</sub> = AG<sub>YX</sub>.

### get_final_AT_allcross.m

It calculates the final single-criterion analogy matrix for tectonic setting. It requires to load the file [ATmatrices.mat](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_mat_files/data_mats/ATmatrices.mat), which is derived
from the script [votw_analysis.m](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts/votw_analysis.m).

### get_final_AG_allcross.m

It calculates the final single-criterion analogy matrix for rock geochemistry. It requires to load the file [AGmatrices_ALU_QUET.mat](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_mat_files/data_mats/AGmatrices_ALU_QUET.mat), which is
derived from the script [votw_analysis.m](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts/votw_analysis.m).

### get_final_AM_allcross.m

It calculates the final single-criterion analogy matrix for volcano morphology. It requires to load the file [AMmatrices_QUET.mat](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_mat_files/data_mats/AMmatrices_QUET.mat), which is
derived from the script [morphology_processing.m](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts/morphology_processing.m).

### get_final_ASz_allcross.m

It calculates the final single-criterion analogy matrix for eruption size. It requires to load the file [ASzmatrices_SINA.mat](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_mat_files/data_mats/ASzmatrices_SINA.mat), which is
derived from the script [eruption_size_processing.m](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts/eruption_size_processing.m).

### get_final_ASt_allcross.m

It calculates the final single-criterion analogy matrix for eruption style. It requires to load the file [AStmatrices_SINA.mat](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_mat_files/data_mats/AStmatrices_SINA.mat), which is
derived from the script [eruption_style_processing.m](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_matlab_scripts/eruption_style_processing.m).

### votw_analysis.m

It performs a preliminary analysis of the volcano data in the GVP database (v4.6.7), and derives the data required to calculate the single-criterion analogy matrices for tectonic setting and rock geochemistry. It requires to import the data in the file: [VOTW467_8May18_volcano_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv) to carry out the aforementioned tasks. Please see below for a brief description of the csv files.

### morphology_processing.m

It performs a preliminary analysis of the morphology databases used by VOLCANS:
[Pike and Clow (1981)](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume)
and [Grosse et al. (2014)](https://doi.org/10.1007/s00445-013-0784-4), and derives the data required to calculate the single-criterion analogy matrix for volcano morphology.
It requires to import the data in the files: [PC81_GR2014_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/PC81_GR2014_data.csv), and [VOTW467_8May18_volcano_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv) to carry out the aforementioned tasks.
Please see below for a brief description of the csv files.

### eruption_size_processing.m

It derives the data required to calculate the single-criterion analogy matrix for eruption size. It requires to import the data in the files:
[VOTW467_8May18_eruption_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_eruption_data.csv), [VOTW467_8May18_volcano_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv), and [MeadMagill2014_June2018.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/MeadMagill2014_June2018.csv) to carry out the aforementioned task.
Please see below for a brief description of the csv files, and [Methods](https://link.springer.com/article/10.1007/s00445-019-1336-3#Sec6) in Tierz et al. (2019)
for more details on the procedure applied in `VOLCANS` to account for under-recording of eruptions.

### eruption_style_processing.m

It derives the data required to calculate the single-criterion analogy matrix for eruption style. It requires to import the data in the files:
[VOTW467_8May18_event_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_event_data.csv), [VOTW467_8May18_eruption_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_eruption_data.csv), and [VOTW467_8May18_volcano_data.csv](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/matlab-scripts/pyvolcans/VOLCANS_csv_files/VOTW467_8May18_volcano_data.csv) to carry out the aforementioned task.
Please see below for a brief description of the csv files.

## Data (csv) files

### VOTW467_8May18_volcano_data.csv

It contains the list of Holocene volcanoes in the GVP database (v4.6.7), together with data on their tectonic setting, required to calculate the analogy
with the same name, as well as data on their major and minor rock types: the latter required to calculate the analogy in rock geochemistry.
NB. It corresponds with [ESM2](https://static-content.springer.com/esm/art%3A10.1007%2Fs00445-019-1336-3/MediaObjects/445_2019_1336_MOESM2_ESM.csv) in Tierz et al. (2019).

### VOTW467_8May18_eruption_data.csv

It contains the list of Holocene eruptions from volcanoes in the GVP database (v4.6.7), together with other data required to calculate the analogy in
eruption size (e.g. Volcanic Explosivity Index or eruption date).
NB. It corresponds with [ESM3](https://static-content.springer.com/esm/art%3A10.1007%2Fs00445-019-1336-3/MediaObjects/445_2019_1336_MOESM3_ESM.csv) in Tierz et al. (2019).

### VOTW467_8May18_event_data.csv

It contains the list of ''eruptive events'' during Holocene eruptions at volcanoes in the GVP database (v4.6.7), together with their grouping according to different hazardous phenomena: the latter required to calculate the analogy in eruption style (please see [Methods](https://link.springer.com/article/10.1007/s00445-019-1336-3#Sec6) in Tierz et al., 2019,
for more details).
NB. It corresponds with [ESM4](https://static-content.springer.com/esm/art%3A10.1007%2Fs00445-019-1336-3/MediaObjects/445_2019_1336_MOESM4_ESM.csv) in Tierz et al. (2019). 

### MeadMagill2014_June2018.csv

It contains the median values for the date of completeness (i.e. date after which the eruptive record for a given volcano is considered complete) extracted
from [Table 1](https://link.springer.com/article/10.1007/s00445-014-0874-y/tables/1) in Mead and Magill (2014).

### PC81_GR2014_data.csv

It contains the list of Holocene volcanoes in the GVP database (v4.6.7) for which there is morphological data available in the
[Pike and Clow (1981)](https://www.researchgate.net/publication/259487495_Revised_classification_of_terrestrial_volcanoes_and_catalog_of_topographic_dimensions_with_new_results_on_edifice_volume)
and [Grosse et al. (2014)](https://doi.org/10.1007/s00445-013-0784-4) volcano morphology databases. These data are used to calculate the analogy in volcano morphology.
NB. It corresponds with [ESM5](https://static-content.springer.com/esm/art%3A10.1007%2Fs00445-019-1336-3/MediaObjects/445_2019_1336_MOESM5_ESM.csv) in Tierz et al. (2019).

## Authorship and Licence

`VOLCANS` was devised by [Pablo Tierz](https://www.bgs.ac.uk/people/tierz-lopez-pablo/) ([@PTierz](https://github.com/PTierz)),
[Susan C. Loughlin](https://www.bgs.ac.uk/people/loughlin-susan/) (British Geological Survey),
and [Eliza S. Calder](https://www.research.ed.ac.uk/en/persons/eliza-calder) (University of Edinburgh).
All Matlab scripts were written by [Pablo Tierz](https://www.bgs.ac.uk/people/tierz-lopez-pablo/) ([@PTierz](https://github.com/PTierz)).

`PyVOLCANS` and the associated VOLCANS Matlab scripts are distributed under the [LGPL v3.0 licence](https://github.com/BritishGeologicalSurvey/pyvolcans/blob/main/LICENSE).
Copyright: © BGS / UKRI 2021.

