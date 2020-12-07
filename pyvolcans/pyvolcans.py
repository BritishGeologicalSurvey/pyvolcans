# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:13:20 2020

@author: Pablo Tierz, John A. Stevenson, Vyron Christodoulou
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""

#Pytonic order
#standard library
import argparse
import logging
import sys
#personal packages
from pyvolcans.pyvolcans_func import (
    _frac_to_float,
    get_volcano_name_from_volcano_number,
    calculate_weighted_analogy_matrix,
    get_analogies,
    get_many_analogy_percentiles,
    PyvolcansError
)

from pyvolcans import __version__

def cli():
    """
    Command line interface to run PyVOLCANS and return analogues.
    """
    # Setup logging
    formatter = logging.Formatter('pyvolcans: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler], level=logging.INFO)

    #getting the arguments
    args = parse_args()

    #get volcano_name from volcano arg
    try:
        volcano_id = int(args.volcano)
        volcano_name = get_volcano_name_from_volcano_number(volcano_id)
    except ValueError:
        volcano_name = args.volcano
    except PyvolcansError as exc:
        # Print error message and quit program on error
        logging.error(exc.args[0])
        sys.exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    #defining some intermediate variables
    count = args.count
    arg_weights = {'tectonic_setting': _frac_to_float(args.tectonic_setting),
                   'geochemistry': _frac_to_float(args.rock_geochemistry),
                   'morphology': _frac_to_float(args.morphology),
                   'eruption_size': _frac_to_float(args.eruption_size),
                   'eruption_style': _frac_to_float(args.eruption_style)}

    my_apriori_volcanoes = args.apriori

    logging.debug("Supplied arguments: %s", args)
    logging.debug("Arg weights as float: %s", arg_weights)

    # Call pyvolcans
    try:
        # calculated_weighted_analogy_matrix
        my_weighted_matrix = calculate_weighted_analogy_matrix(
            weights=arg_weights)

        # calling the get_analogies function to derive the final data
        get_analogies(volcano_name, my_weighted_matrix, count)

        # calling the get_many_analogy_percentiles function
        # to print 'better analogues'
        if my_apriori_volcanoes is not None:
            get_many_analogy_percentiles(volcano_name,
                                         my_apriori_volcanoes,
                                         my_weighted_matrix)
    except PyvolcansError as exc:
        # Print error message and quit program on error
        logging.error(exc.args[0])
        sys.exit(1)

def parse_args():
    """
    Reads PyVOLCANS arguments from command line and returns values
    that are usable by the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("volcano",
                        help="Set target volcano name or Smithsonian ID",
                        type=str)
    parser.add_argument("--apriori", nargs='*',
                        help="Provide one or more a priori analogue volcanoes",
                        default=None)
    parser.add_argument("--tectonic_setting",
                        help=
                        "Set tectonic setting weight (e.g. '0.2' or '1/5')",
                        default='0.2', type=str)
    parser.add_argument("--rock_geochemistry",
                        help=
                        "Set rock geochemistry weight (e.g. '0.2' or '1/5')",
                        default='0.2', type=str)
    parser.add_argument("--morphology",
                        help=
                        "Set volcano morphology weight (e.g. '0.2' or '1/5')",
                        default='0.2', type=str)
    parser.add_argument("--eruption_size",
                        help=
                        "Set eruption size weight (e.g. '0.2' or '1/5')",
                        default='0.2', type=str)
    parser.add_argument("--eruption_style",
                        help=
                        "Set eruption style weight (e.g. '0.2' or '1/5')",
                        default='0.2', type=str)
    parser.add_argument("--count",
                        help="Set the number of top analogue volcanoes",
                        default='10', type=int)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print debug-level logging output")
    parser.add_argument("--version", "-V", action="version",
                        help="Show package version",
                        version=__version__)
    #'parsing the arguments'
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cli()
    