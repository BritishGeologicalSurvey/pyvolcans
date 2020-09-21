# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:49:16 2020

@author: pablo
"""

#set of functions related to the implementation of PyVOLCANS

#we need to read a csv file here
#standard packages
from pathlib import Path
from fractions import Fraction
#external packages
from pymatreader import read_mat
import pandas as pd
import numpy as np
from scipy import stats
import webbrowser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#from pyvolcans import tectonic_analogy
#geochemistry_analogy,
#morphology_analogy, eruption_size_analogy, eruption_style_analogy)

#remember we have no header in the file below
volcano_names = pd.read_csv("VOLCANS_mat_files/VOTW_prepared_data/" +
                            "volc_names.csv", header = None)

#dictionary of weights for the criteria
WEIGHTS = {'tectonic_setting': 0.2, 'geochemistry': 0.2,
           'morphology': 0.2, 'eruption_size': 0.2, 'eruption_style': 0.2}
#loading all the data
ANALOGY_DIR = Path("VOLCANS_mat_files/analogy_mats")

def _frac_to_float(value):
    """Take a string of decimal or fractional number (e.g. '0.5' or '1/2')
       and return the float representation."""
    return float(Fraction(value))


def fuzzy_matching(volcano_name, limit=10):
    """
    List volcanoes with names most similar to volcano_name.

    :param volcano_name: str, name of volcano
    :param limit: int, number of values to return
    :return names: list of str of similar names
    """
    matches = process.extract(volcano_name, volcano_names[0], limit=limit,
                              scorer=fuzz.UQRatio)
    names = [item[0] for item in matches]
    return names


def get_volcano_idx_from_name(volcano_name):
    """
    Input is volcano name as text, output is the index 
    of the row/column with the volcano in the matrix.
    """
    ##we need to create a message error here: "Name provided doesn't exist.
    ###"Please double-check spelling (including commas, e.g. "Ruiz, Nevado del"
    ###and/or check name on www.volcano.si.edu"
    
    matched_volcanoes = match_name(volcano_name)    
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

    matched_volcanoes = match_name(volcano_name)        
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

def calculate_weighted_analogy_matrix(weights = WEIGHTS,
                                      analogy_dir = ANALOGY_DIR):
    """
    Input is dictionary of weights
    e.g. {‘tectonic_setting’: 0.5, ‘geochemistry’: 0.5}
    returns numpy array of weighted matrix.
    NB. We load all the matrices here inside the function
    """
  
    tectonic_analogy = read_mat(analogy_dir / 
                            "ATfinal_allvolcs.mat")['AT_allcross']
    geochemistry_analogy = read_mat(analogy_dir / 
                                "AGfinal_allvolcs_ALU.mat")['AG_allcross']
    morphology_analogy = read_mat(analogy_dir / 
                              "AMfinal_allvolcs.mat")['AM_allcross']
    eruption_size_analogy = read_mat(analogy_dir / 
                                 "ASzfinal_allvolcs_SINA.mat")['ASz_allcross']
    eruption_style_analogy = read_mat(analogy_dir / 
                                  "AStfinal_allvolcs_SINA.mat")['ASt_allcross']
    
    #ERROR HANDLING!! (AND TEST!!!)
    if sum(weights.values()) != 1:
        msg = f"Sum of weights is different from 1!" 
        raise PyvolcansError(msg)        
    
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

def get_analogies(my_volcano, weighted_analogy_matrix, count=10):
    """
    Returns, on screen, the names of the top <count> analogues to
    the target volcano (i.e. my_volcano) and their multi-criteria
    analogy values, as a variable: total_analogy.
    Default <count> = 10.
    """
    
    #get the index for my_volcano
    volcano_idx = get_volcano_idx_from_name(my_volcano)
    
    #calculate the <count> highest values of multi-criteria analogy
    #getting the row corresponding to the target volcano ('my_volcano') 
    my_volcano_analogies = weighted_analogy_matrix[volcano_idx,]
    #adding 1 to 'count' to consider 'my_volcano' itself in the search
    count = count+1
    #getting the indices corresponding to the highest values of analogy
    #in descending order (highest analogy first)
    top_idx = my_volcano_analogies.argsort()[-count:][::-1]
    ##removing 'my_volcano' from the list
    ##top_idx = set(volcano_idx).symmetric_difference(top_idx)
    ##np.argpartition(my_volcano_analogies, \
    ##len(my_volcano_analogies) - count)[-count:]
    
    # obtain the volcano names and the analogy values
    top_analogies = my_volcano_analogies[top_idx]
    
    #print the names of the top <count> analogues
    ##print(volcano_names.iloc[top_idx,2],volcano_names.iloc[top_idx,0:1],
      ##     top_analogies)
      
    print(volcano_names.iloc[top_idx,0:3])
    
    for ii in range(len(top_idx)):
        #print('%d\t%s\t%s\t%.3f\n' %
        print(f'{volcano_names.iloc[top_idx[ii],2]:d}\t\
                 {volcano_names.iloc[top_idx[ii],0]:s}\t\
                 {volcano_names.iloc[top_idx[ii],1]:s}\t\
                 {top_analogies[ii]:.3f}')
    
    #open the GVP website of the top 1 analogue
    top_analogue_vnum = volcano_names.iloc[top_idx[1],2] #[0]=target volcano!!
    my_web = f'https://volcano.si.edu/volcano.cfm?vn={top_analogue_vnum}' \
                '&vtab=GeneralInfo' #Getting to open the General Info tab
    webbrowser.open(my_web)
    
    #here: return the analogy values
    pass
    

def match_name(volcano_name):
    matched_volcanoes = volcano_names.loc[volcano_names[0] == volcano_name]
    #throw errors whether if volcano does not exist
    #or there are 2+ identical names
    if len(matched_volcanoes) == 0:
        name_suggestions = fuzzy_matching(volcano_name)
        suggestions_string = "\n".join(name_suggestions)
        msg = (f'"{volcano_name}" not found! Did you mean:\n{suggestions_string}')
        raise PyvolcansError(msg)        
    elif len(matched_volcanoes) > 1:
        msg = f"Volcano name {volcano_name} is not unique!" 
        raise PyvolcansError(msg)
    
    return matched_volcanoes


def get_analogy_percentile(my_volcano, apriori_volcano,
                           weighted_analogy_matrix):
    """
    This function takes the target volcano (my_volcano), one 'a priori'
    analogue volcano (apriori_volcano), and the weighted analogy matrix
    calculated for the target volcano (weighted_analogy_matrix), and
    returns one percentile.
    This percentile corresponds to the analogy value between the
    target volcano and the a priori analogue within the distribution of
    analogy values between the target volcano and any Holocene volcano
    in the GVP database.
    :param my_volcano: str
    :param apriori_volcano: str
    :param weighted_analogy_matrix: numpy array     
    :return percentile: float
    """
    #convert volcano names into inds to access the weighted_analogy_matrix
    my_volcano_idx=get_volcano_idx_from_name(my_volcano)
    apriori_volcano_idx=get_volcano_idx_from_name(apriori_volcano)
    
    #derive a vector with the analogy values for the target volcano
    my_analogy_values=weighted_analogy_matrix[my_volcano_idx,]
    
    #calculate percentiles from 0 to 100 (like in VOLCANS for now)
    analogy_percentiles=np.percentile(my_analogy_values,np.linspace(0,100,101))
    
    #find the closest value to the analogy of the a priori volcano
    #NOTE that this value already represents the percentile (0-100)
    my_percentile = (np.abs(analogy_percentiles - \
                            my_analogy_values[apriori_volcano_idx])).argmin()
    
    #Possible steps:
    return my_percentile

def get_many_analogy_percentiles(my_volcano, apriori_volcanoes_list,
                                 weighted_analogy_matrix):
    """
    This function takes the target volcano (my_volcano), a collection
    of one or more 'a priori' analogue volcanoes in a list
    (apriori_volcanoes_list), and the weighted analogy matrix calculated
    for the target volcano (weighted_analogy_matrix), and returns a
    collection of percentiles (as many as a priori analogues).
    These percentiles correspond to those of the analogy value between
    the target volcano and the a priori analogue within the distribution
    of analogy values between the target volcano and any Holocene volcano
    in the GVP database.
    :param my_volcano: str
    :param apriori_volcano: list of str
    :param weighted_analogy_matrix: numpy array     
    :return percentile: dict of apriori volcano name and percentile
    :return better_analogues: dict of 'better analogues' name and percentage    
    """
    
    #check a priori volcanoes is a list
    if not isinstance(apriori_volcanoes_list, list):
        raise PyvolcansError("A priori volcanoes should be a list!")
    
    percentile_dictionary = {}
    better_analogues_dictionary = {} #100-percentile
    
    #loop over get_analogy_percentile
    for volcano in apriori_volcanoes_list:
        percentile = get_analogy_percentile(my_volcano, volcano,
                                            weighted_analogy_matrix)
        percentile_dictionary[volcano] = percentile
        better_analogues_dictionary[volcano] = 100 - percentile
    
    #adding a 'printing functionality' to the function
    print('\n\nAccording to PyVOLCANS, the following percentages of volcanoes'
          +f' in the GVP database\nare better analogues to {my_volcano:s}'
          +' than the a priori analogues reported below:\n')
    for volcano, percentage in better_analogues_dictionary.items():
        print(f'{volcano:s}: {percentage:d}%\n')
    
    return percentile_dictionary, better_analogues_dictionary



class PyvolcansError(Exception):
    pass


    
