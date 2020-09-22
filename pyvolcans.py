# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:13:20 2020

@author: pablo
"""

#import scipy.io as sio
#matfile = sio.loadmat("VOLCANS_mat_files/analogy_mats/ATfinal_allvolcs.mat")

#Pytonic order
#standard library
import argparse
import logging
from pathlib import Path
from fractions import Fraction
#external packages
from pymatreader import read_mat
#personal packages
from pyvolcans_func import (_frac_to_float, get_analogies,
calculate_weighted_analogy_matrix, get_many_analogy_percentiles)
#import pyvolcans_func

# Setup logging
formatter = logging.Formatter('pyvolcans: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(handlers=[handler], level=logging.INFO)

#loading the files required to calculate analogies and analogue volcanoes
#ANALOGY_DIR = Path("VOLCANS_mat_files/analogy_mats")
#
#tectonic_analogy = read_mat(ANALOGY_DIR / 
#                        "ATfinal_allvolcs.mat")['AT_allcross']
#geochemistry_analogy = read_mat(ANALOGY_DIR / 
#                            "AGfinal_allvolcs_ALU.mat")['AG_allcross']
#morphology_analogy = read_mat(ANALOGY_DIR / 
#                          "AMfinal_allvolcs.mat")['AM_allcross']
#eruption_size_analogy = read_mat(ANALOGY_DIR / 
#                             "ASzfinal_allvolcs_SINA.mat")['ASz_allcross']
#eruption_style_analogy = read_mat(ANALOGY_DIR / 
#                              "AStfinal_allvolcs_SINA.mat")['ASt_allcross']

#var1 = print('Select the weight for tectonic setting')
#var2
#...
#var5
#
#weights = {var1,...,var5}
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("volcano_name",
                        help="Set target volcano",
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

    #'parsing the arguments'
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    #defining some intermediate variables
    volcano_name = args.volcano_name
    count = args.count
    arg_weights = {'tectonic_setting': _frac_to_float(args.tectonic_setting),
               'geochemistry': _frac_to_float(args.rock_geochemistry),
               'morphology': _frac_to_float(args.morphology),
               'eruption_size': _frac_to_float(args.eruption_size),
               'eruption_style': _frac_to_float(args.eruption_style)}

    my_apriori_volcanoes = args.apriori

    logging.debug("Supplied arguments: %s", args)
    logging.debug("Arg weights as float: %s", arg_weights)

    #calculated_weighted_analogy_matrix
    my_weighted_matrix = \
    calculate_weighted_analogy_matrix(weights = arg_weights)
    
    #calling the get_analogies function to derive the final data
    get_analogies(args.volcano_name,my_weighted_matrix,count)
    
    #calling the get_many_analogy_percentiles function
    #to print 'better analogues'
    if my_apriori_volcanoes is not None:
        get_many_analogy_percentiles(args.volcano_name, my_apriori_volcanoes,
                                     my_weighted_matrix)
