"""
    An open-access Python tool that generates data-driven sets of analogue
    volcanoes for any Holocene volcano listed in the Global Volcanism Program
    (GVP) Volcanoes Of The World database (v. 4.6.7), based on the VOLCANS
    (VOLCano ANalogues Search) method presented by Tierz, Loughlin and Calder
    (2019): https://doi.org/10.1007/s00445-019-1336-3

    VOLCANS uses five volcanological criteria (tectonic setting, rock
    geochemistry, volcano morphology, eruption size and eruption style), and
    a structured combination of them, to quantify overall multi-criteria (or
    total) volcano analogy among any two volcanoes in the GVP database.
    The data used by the method are extracted from the GVP database as well as
    from a merged database of volcano morphology (after Pike and Clow, 1981;
    Grosse et al., 2014).

    PyVOLCANS provides its user with full flexibility to identify customised
    sets of analogue volcanoes, by exploring three main variables:

        (1) target volcano (or volcano of interest);
        (2) weighting scheme (i.e. set of weights given to each of the five
        volcanological criteria to calculate multi-criteria, total analogy);
        (3) number of 'top' analogue volcanoes (i.e. those with the highest
        value of analogy with the target volcano).

    In addition, PyVOLCANS allows the user to compare the values of total
    analogy computed for 'a priori analogues' (i.e. volcanoes thought to be
    good analogues to the target volcano by other strands of evidence, e.g.
    expert knowledge) with those computed for the rest of volcanoes in the GVP
    database. This permits investigation of sets of analogue volcanoes for
    varied purposes, and makes PyVOLCANS a useful complementary method to
    expert-derived analogue volcanoes. Please see Tierz et al. (2019) for more
    details on the VOLCANS method (https://doi.org/10.1007/s00445-019-1336-3).
"""
# flake8: noqa

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from pyvolcans.VOLCANS_mat_files.base import load_volcano_names
from pyvolcans.VOLCANS_mat_files.base import load_tectonic_analogy
from pyvolcans.VOLCANS_mat_files.base import load_geochemistry_analogy
from pyvolcans.VOLCANS_mat_files.base import load_morphology_analogy
from pyvolcans.VOLCANS_mat_files.base import load_eruption_style_analogy
from pyvolcans.VOLCANS_mat_files.base import load_eruption_size_analogy
