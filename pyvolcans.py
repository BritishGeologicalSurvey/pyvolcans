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
from fractions import Fraction
#external packages
from pymatreader import read_mat
#personal packages
from pyvolcans_func import get_analogies, calculate_weighted_analogy_matrix
#import pyvolcans_func

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
    parser.add_argument("--tectonic_setting",
                        help="Set tectonic setting weight",
                        default='0.2', type=str)
    parser.add_argument("--rock_geochemistry",
                        help="Set rock geochemistry weight",
                        default='0.2', type=str)
    parser.add_argument("--morphology",
                        help="Set volcano morphology weight",
                        default='0.2', type=str)
    parser.add_argument("--eruption_size",
                        help="Set eruption size weight",
                        default='0.2', type=str)
    parser.add_argument("--eruption_style",
                        help="Set eruption style weight",
                        default='0.2', type=str)
    parser.add_argument("--count",
                        help="Set the number of top analogue volcanoes",
                        default='10', type=str)
    
    #'parsing the arguments'
    args = parser.parse_args()
    
    #here we convert all required inputs from str to float/int
    #NB. We need to check whether the weight input by the user is
    #    a fraction or not. We'll use str.find() to check for this
    if args.tectonic_setting.find('/') != -1:
        tectonic_setting_weight = float(Fraction(args.tectonic_setting))
    else:
        tectonic_setting_weight = float(args.tectonic_setting)
        
    if args.rock_geochemistry.find('/') != -1:
        rock_geochemistry_weight = float(Fraction(args.rock_geochemistry))
    else:
        rock_geochemistry_weight = float(args.rock_geochemistry)
        
    if args.morphology.find('/') != -1:
        morphology_weight = float(Fraction(args.morphology))
    else:
        morphology_weight = float(args.morphology)
        
    if args.eruption_size.find('/') != -1:
        eruption_size_weight = float(Fraction(args.eruption_size))
    else:
        eruption_size_weight = float(args.eruption_size)
    
    if args.eruption_style.find('/') != -1:
        eruption_style_weight = float(Fraction(args.eruption_style))
    else:
        eruption_style_weight = float(args.eruption_style)    
    
    #defining some intermediate variables
    volcano_name = args.volcano_name
    ARGWEIGHTS = {'tectonic_setting': tectonic_setting_weight,
               'geochemistry': rock_geochemistry_weight,
               'morphology': morphology_weight,
               'eruption_size': eruption_size_weight,
               'eruption_style': eruption_style_weight}
        
    print(args)
    print(volcano_name)
    print(ARGWEIGHTS)
    print(args.rock_geochemistry)
    
    #calculated_weighted_analogy_matrix
    my_weighted_matrix = \
    calculate_weighted_analogy_matrix(weights = ARGWEIGHTS)
    
    #calling the get_analogies function to derive the final data
    get_analogies(args.volcano_name,my_weighted_matrix,args.count)