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
from pyvolcans_func import get_analogies
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
     
    
       
    args = parser.parse_args()
    tectonic_setting = args.tectonic_setting 
    print(args)
#    calculated_weighted_analogy_matrix(tectonic_setting)
    #get_analogies(args.volcano_name)