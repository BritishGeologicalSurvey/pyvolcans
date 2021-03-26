"""
GENERAL DESCRIPTION FOR THE PACKAGE!! WHAT VOLCANS IS, A BIT OF WHY IT WAS
CREATED.
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from pyvolcans.VOLCANS_mat_files.base import load_volcano_names
from pyvolcans.VOLCANS_mat_files.base import load_tectonic_analogy
from pyvolcans.VOLCANS_mat_files.base import load_geochemistry_analogy
from pyvolcans.VOLCANS_mat_files.base import load_morphology_analogy
from pyvolcans.VOLCANS_mat_files.base import load_eruption_style_analogy
from pyvolcans.VOLCANS_mat_files.base import load_eruption_size_analogy

