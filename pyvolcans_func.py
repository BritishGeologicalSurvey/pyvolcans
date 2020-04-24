# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:49:16 2020

@author: pablo
"""

#set of functions related to the implementation of PyVOLCANS

#we need to read a csv file here
import pandas as pd
import numpy as np

from pyvolcans import tectonic_analogy, geochemistry_analogy, \
morphology_analogy, eruption_size_analogy, eruption_style_analogy

#remember we have no header in the file below
volcano_names = pd.read_csv("VOLCANS_mat_files/VOTW_prepared_data/" +
                            "volc_names.csv", header = None)

#dictionary of weights for the criteria
WEIGHTS = {'tectonic_setting': 0.2, 'geochemistry': 0.2,
           'morphology': 0.2, 'eruption_size': 0.2, 'eruption_style': 0.2}


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

    volcano_vnum = matched_volcanoes.iloc[0,2]      
        
    return volcano_vnum

def get_volcano_name_from_volcano_number(volcano_number):
    """
    Input is volcano number as indicated by the GVP,
    output is the volcano name.
    """
    ##we need to create a message error here: "Volcano number does not exist.
    ##Please provide a non-zero, positive, six digits number. To check for
    ##existing volcano numbers (VNUM), please visit www.volcano.si.edu"
    
    matched_volcanoes = volcano_names.loc[volcano_names[2] == volcano_number]
    
    if len(matched_volcanoes) == 0:
        msg = f"Volcano number {volcano_number} does not exist!" 
        raise PyvolcansError(msg)
    #NB. This error below should never occur because VNUM should be unique
    elif len(matched_volcanoes) > 1:
        msg = f"Volcano number {volcano_number} is not unique!" 
        raise PyvolcansError(msg)
    
    volcano_name = \
        matched_volcanoes.iloc[0,0]
    
    return volcano_name

def calculate_weighted_analogy_matrix(weights = WEIGHTS):
    
    """
    Input is dictionary of weights
    e.g. {‘tectonic_setting’: 0.5, ‘geochemistry’: 0.5}
    returns numpy array of weighted matrix
    """
    #COMPLETE!!
    #ERROR HANDLING!! (AND TEST!!!)
    
    weighted_tectonic_analogy = \
        weights['tectonic_setting'] * tectonic_analogy
    
    weighted_geochemistry_analogy = \
        weights['geochemistry'] * geochemistry_analogy
        
    weighted_morphology_analogy = \
        weights['morphology'] * morphology_analogy
        
    weighted_eruption_size_analogy = \
        weights['eruption_size'] * eruption_size_analogy
    
    weighted_eruption_style_analogy = \
        weights['eruption_style'] * eruption_style_analogy
    
    weighted_total_analogy_matrix = weighted_tectonic_analogy + \
        weighted_geochemistry_analogy + weighted_morphology_analogy + \
        weighted_eruption_size_analogy + weighted_eruption_style_analogy
    
    #print(weighted_tectonic_analogy[100,100])
    #print(weighted_geochemistry_analogy[110,110])
    #print(weighted_morphology_analogy[2,2])
    #print(weighted_eruption_size_analogy[9,9])
    #print(weighted_eruption_style_analogy[20,20])
    
    print(weighted_total_analogy_matrix[100,100])
    
    return weighted_total_analogy_matrix

def get_analogies(my_volcano, weighted_analogy_matrix, count=5):
    [returns the names best <count> analogies (and their scores?).  Default = 5.



class PyvolcansError(Exception):
    pass


    