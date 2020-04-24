# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:13:20 2020

@author: pablo
"""

#import scipy.io as sio
#matfile = sio.loadmat("VOLCANS_mat_files/analogy_mats/ATfinal_allvolcs.mat")

from pymatreader import read_mat
from pathlib import Path
import argparse


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
    parser.add_argument("--tectonic_setting", help="Set tectonic setting, default value=0.2")
       
    args = parser.parse_args()
    tectonic_setting = args.tectonic_setting 
#    calculated_weighted_analogy_matrix(tectonic_setting)