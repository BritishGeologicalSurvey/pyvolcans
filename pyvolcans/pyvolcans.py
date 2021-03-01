# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:13:20 2020

@author: Pablo Tierz, John A. Stevenson, Vyron Christodoulou
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""

# Standard library
import argparse
import logging
import sys

# Our packages
from pyvolcans.pyvolcans_func import (
    _frac_to_float,
    calculate_weighted_analogy_matrix,
    get_analogies,
    get_many_analogy_percentiles,
    PyvolcansError,
    set_weights_from_args,
    open_gvp_website,
    output_result,
    VOLCANO_NAMES
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

    # getting the arguments
    args = parse_args()

    # get volcano_name from volcano arg
    try:
        volcano_input = int(args.volcano)
    except ValueError:
        volcano_input = args.volcano
    except PyvolcansError as exc:
        # Print error message and quit program on error
        logging.error(exc.args[0])
        sys.exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # defining some intermediate variables
    count = args.count
    arg_weights = {'tectonic_setting': _frac_to_float(args.tectonic_setting),
                   'geochemistry': _frac_to_float(args.rock_geochemistry),
                   'morphology': _frac_to_float(args.morphology),
                   'eruption_size': _frac_to_float(args.eruption_size),
                   'eruption_style': _frac_to_float(args.eruption_style)}
    try:
        new_weights = set_weights_from_args(arg_weights)
    except PyvolcansError as exc:
        # Print error message and quit program on error
        logging.error(exc.args[0])
        sys.exit(1)    
    my_apriori_volcanoes = args.apriori
    logging.debug("Supplied weights: %s", new_weights)

    # Call pyvolcans
    try:
        # calculated_weighted_analogy_matrix
        volcans_result = calculate_weighted_analogy_matrix(
             volcano_input, weights=new_weights)

        # calling the get_analogies function to derive the final data
        [top_analogues_idx,
        top_analogues,
        volcano_name] = get_analogies(
                                     volcano_input,
                                     volcans_result,
                                     count)
        #return the result
        result = output_result(verbose=args.verbose,
                               my_volcano=volcano_name,
                               result=top_analogues)
        print(result)
        #calling the function to open the GVP website
        if args.website:
            # .iloc[0]=target volcano!! (in principle; we need to fix this)
            top_analogue_vnum = VOLCANO_NAMES.iloc[top_analogues_idx.iloc[1],2]
            try:
                open_gvp_website(top_analogue_vnum)
            except PyvolcansError as exc:
                logging.warn(exc.args[0])

        #calling the function to write the top analogues to a csv file
        if args.write_csv_file:
            result = output_result(args.verbose,
                                   volcano_name,
                                   top_analogues,
                                   to_file='csv')
        # calling the get_many_analogy_percentiles function
        # to print 'better analogues'
        if my_apriori_volcanoes is not None:
            get_many_analogy_percentiles(volcano_input,
                                         my_apriori_volcanoes,
                                         volcans_result)
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
    parser.add_argument("-Ts","--tectonic_setting",
                        help=
                        "Set tectonic setting weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-G","--rock_geochemistry",
                        help=
                        "Set rock geochemistry weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-M","--morphology",
                        help=
                        "Set volcano morphology weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-Sz","--eruption_size",
                        help=
                        "Set eruption size weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-St","--eruption_style",
                        help=
                        "Set eruption style weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("--count",
                        help="Set the number of top analogue volcanoes",
                        default='10', type=int)
    parser.add_argument("-w", "--write_csv_file", action="store_true",
                        help=
                        "Write list of top analogue volcanoes as .csv file")
    parser.add_argument("-W", "--website", action="store_true",
                        help="Open GVP website for top analogue volcano")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print debug-level logging output")
    parser.add_argument("-V", "--version", action="version",
                        help="Show package version",
                        version=__version__)

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cli()
