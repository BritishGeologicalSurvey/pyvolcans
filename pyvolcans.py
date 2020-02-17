# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:13:20 2020

@author: pablo
"""

#import scipy.io as sio
#matfile = sio.loadmat("VOLCANS_mat_files/analogy_mats/ATfinal_allvolcs.mat")

from pymatreader import read_mat
from pathlib import Path

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