project = 'PyVOLCANS'
copyright = 'GNU Lesser General Public License v3.0'
author = 'Pablo Tierz, Vyron Christodoulou, John A Stevenson'

from pyvolcans import __version__
version =  __version__
release = __version__.split('.')[1]
templates_path = ['_templates']
extensions =  ["myst_parser"]
source_suffix = ['.rst', '.md']
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = []
