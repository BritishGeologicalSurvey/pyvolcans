# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:49:16 2020

@author: pablo
"""

#set of functions related to the implementation of PyVOLCANS

#we need to read a csv file here
import pandas as pd

#remember we have no header in the file below
volcano_names = pd.read_csv("VOLCANS_mat_files/VOTW_prepared_data/" +
                            "volc_names.csv", header = None)

def get_volcano_idx_from_name(volcano_name):
    """
    Input is volcano name as text, output is the index 
    of the row/column with the volcano in the matrix.
    """
    ##we need to create a message error here: "Name provided doesn't exist.
    ###"Please double-check spelling (including commas, e.g. "Ruiz, Nevado del"
    ###and/or check name on www.volcano.si.edu"
    
    matched_volcanoes = volcano_names.loc[volcano_names[0] == volcano_name]
    
    if len(matched_volcanoes) == 0:
        msg = f"Volcano name {volcano_name} does not exist!" 
        raise PyvolcansError(msg)
    elif len(matched_volcanoes) > 1:
        msg = f"Volcano name {volcano_name} is not unique!" 
        raise PyvolcansError(msg)

    volcano_index = matched_volcanoes.index[0]        
        
    return volcano_index

def get_volcano_name_from_idx(volcano_idx):
    """
    Input is volcano index as a number, output is the name 
    of the volcano of interest.
    NB. Is it better to use Python indexing (starting in zero) or not,
    if the 'volcano_idx' is input by the user?
    """
    ##we need to create a message error here: "Volcano index out of bounds.
    ##Please provide a non-zero, positive number smaller than 1439 (Number of
    ##volcanoes in VOTW 4.6.7 database)."
    
    volcano_name = \
        volcano_names.iloc[volcano_idx,0]
    
    return volcano_name

def get_volcano_number_from_name(volcano_name):
    """
    Input is volcano name as text, output is the volcano 
    number as indicated in the GVP database.
    """
    pass

def get_volcano_name_from_volcano_number(volcano_number):
    """
    Input is volcano number as indicated by the GVP,
    output is the volcano name.
    """
    pass

class PyvolcansError(Exception):
    pass

    
    