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
from pathlib import Path
#external packages
from pymatreader import read_mat
#personal packages
from pyvolcans_func import get_analogies, calculate_weighted_analogy_matrix
#import pyvolcans_func

ANALOGY_DIR = Path("VOLCANS_mat_files/analogy_mats")

tectonic_analogy = read_mat(ANALOGY_DIR / 
                            "ATfinal_allvolcs.mat")['AT_allcross']
geochemistry_analogy = read_mat(ANALOGY_DIR / 
                                "AGfinal_allvolcs_ALU.mat")['AG_allcross']
morphology_analogy = read_mat(ANALOGY_DIR / 
                              "AMfinal_allvolcs.mat")['AM_allcross']
eruption_size_analogy = read_mat(ANALOGY_DIR / 
                                 "ASzfinal_allvolcs_SINA.mat")['ASz_allcross']
eruption_style_analogy = read_mat(ANALOGY_DIR / 
                                  "AStfinal_allvolcs_SINA.mat")['ASt_allcross']

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
    parser.add_argument("--tectonic_setting",
                        help="Set tectonic setting weight",
                        default=0.2, type=float)
    parser.add_argument("--rock_geochemistry",
                        help="Set rock geochemistry weight",
                        default=0.2, type=float)
    parser.add_argument("--morphology",
                        help="Set volcano morphology weight",
                        default=0.2, type=float)
    parser.add_argument("--eruption_size",
                        help="Set eruption size weight",
                        default=0.2, type=float)
    parser.add_argument("--eruption_style",
                        help="Set eruption style weight",
                        default=0.2, type=float)
    parser.add_argument("--count",
                        help="Set the number of top analogue volcanoes",
                        default=10, type=int)
       
    args = parser.parse_args()
    volcano_name = args.volcano_name
    ARGWEIGHTS = {'tectonic_setting': args.tectonic_setting,
               'geochemistry': args.rock_geochemistry,
               'morphology': args.morphology,
               'eruption_size': args.eruption_size,
               'eruption_style': args.eruption_style}
        
    print(args)
    print(volcano_name)
    print(ARGWEIGHTS)
    print(args.rock_geochemistry)
    
    #calculated_weighted_analogy_matrix
    my_weighted_matrix = \
    calculate_weighted_analogy_matrix(weights = ARGWEIGHTS)
    
    #calling the get_analogies function to derive the final data
    get_analogies(args.volcano_name,my_weighted_matrix,args.count)