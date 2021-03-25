# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:49:16 2020

@author: Pablo Tierz, John A. Stevenson, Vyron Christodoulou
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""

# set of functions related to the implementation of PyVOLCANS

# standard packages
import logging
import sys
import webbrowser
from pathlib import Path
from fractions import Fraction

# external packages
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from pyvolcans import (load_tectonic_analogy,
                       load_geochemistry_analogy,
                       load_morphology_analogy,
                       load_eruption_size_analogy,
                       load_eruption_style_analogy,
                       load_volcano_names)

VOLCANO_NAMES = load_volcano_names()

#dictionary of weights for the criteria
WEIGHTS = {'tectonic_setting': 0.2, 'geochemistry': 0.2,
           'morphology': 0.2, 'eruption_size': 0.2, 'eruption_style': 0.2}

# loading all the data
ANALOGY_MATRIX = {'tectonic_setting': load_tectonic_analogy(),
                  'geochemistry': load_geochemistry_analogy(),
                  'morphology': load_morphology_analogy(),
                  'eruption_size': load_eruption_size_analogy(),
                  'eruption_style': load_eruption_style_analogy()
                  }


def _frac_to_float(value):
    """Converts a string of decimal or fractional number (e.g. '0.5' or '1/2')
       into a floating-point representation.

    Parameters
    ----------
    value : str

    Returns
    -------
    value_as_float : float

    Raises
    ------
    PyvolcansError
        If the function is called using a list, instead of a single value.

        If ValueError or ZeroDivisionError exceptions are encountered
        while trying to convert the string into a float. For example,
        if the function is called using a string made up of characters.
    """

    if isinstance(value, list):
        if len(value) > 1:
            msg = ("Some criterion weights are duplicated! "
                   "Please revise your weighting scheme.")
            raise PyvolcansError(msg)
        elif len(value) == 1:
            value = value[0]
       
    if value is None:
        value_as_float = None
    else:
        if '/' in value:
            try:
                numerator, denominator =  value.split('/')
                value_as_float = float(
                        Fraction(numerator) / Fraction(denominator))
            except (ValueError, ZeroDivisionError):
                msg = f"Unable to convert given weight ({value}) to number"
                raise PyvolcansError(msg)
        else:
            try:
                value_as_float = float(Fraction(value))
            except ValueError:
                msg = f"Unable to convert given weight ({value}) to number"
                raise PyvolcansError(msg)

    return value_as_float



def fuzzy_matching(volcano_name, limit=10):
    """Provides a list of volcanoes with names most similar to volcano_name.

    Parameters
    ----------
    volcano_name : str
        Name of volcano introduced by the user (i.e. target volcano)
    limit : int, optional
        Number of names that the function returns

    Returns
    -------
    similar_volcano_names : str
        List of volcanoes with similar names to the target volcano
    """

    matches = process.extract(volcano_name, VOLCANO_NAMES[0], limit=limit,
                              scorer=fuzz.UQRatio)
    match_idx = [item[2] for item in matches]
    volcano_info = VOLCANO_NAMES.iloc[match_idx].rename(columns={0:'name',
                                                                 1:'country',
                                                                 2:'smithsonian_id'})
    similar_volcano_names = volcano_info.to_string(index=False)

    return similar_volcano_names


def get_volcano_idx_from_number(volcano_number):
    """
       Input smithsonian id and get index of the volcano matrix
    """
    volcano_idx = VOLCANO_NAMES.loc[VOLCANO_NAMES[2] == volcano_number]
    if volcano_idx.empty:
        msg = ("Volcano number does not exist. "
               "Please provide a non-zero, positive, six digits number. To check for "
               "existing volcano numbers (VNUM), please visit www.volcano.si.edu")
        raise PyvolcansError(msg)

    return volcano_idx.index[0]


def get_volcano_idx_from_name(volcano_name):
    """
    Input is volcano name as text, output is the index
    of the row/column with the volcano in the matrix.
    """
    # we need to create a message error here: "Name provided doesn't exist.
    # #"Please double-check spelling (including commas, e.g. "Ruiz, Nevado del"
    # #and/or check name on www.volcano.si.edu"

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
    # we need to create a message error here: "Volcano index out of bounds.
    # Please provide a non-zero, positive number smaller than 1439 (Number of
    # volcanoes in VOTW 4.6.7 database)."

    volcano_name = \
        VOLCANO_NAMES.iloc[volcano_idx, 0]

    return volcano_name


def get_volcano_number_from_name(volcano_name):
    """
    Input is volcano name as text, output is the volcano
    number as indicated in the GVP database.
    """
    # we need to create a message error here: "Name provided doesn't exist.
    # #"Please double-check spelling (including commas, e.g. "Ruiz, Nevado del"
    # #and/or check name on www.volcano.si.edu"

    matched_volcanoes = match_name(volcano_name)
    volcano_vnum = matched_volcanoes.iloc[0, 2]
    return volcano_vnum


def convert_to_idx(my_volcano):
    """ 
        Check if input is string or not.
        Convert to index
    """
    if isinstance(my_volcano, str):
        volcano_idx = get_volcano_idx_from_name(my_volcano)
    else:
        volcano_idx = get_volcano_idx_from_number(my_volcano)

    return volcano_idx


def set_weights_from_args(args_dict):
    """
    If no arguments are specified everything is set to 0.2
    """
    no_values_set = all(value is None for value in args_dict.values())

    if no_values_set:
        args_dict = dict.fromkeys(args_dict.keys(), 0.2)
        return args_dict

    sum_of_weights = 0
    for key, value in args_dict.items():
        if value is None:
            args_dict[key] = 0
        else:
            sum_of_weights += value

    if (sum_of_weights < 1-1e-10) or (sum_of_weights > 1+1e-10):
        msg = (f"Sum of weights ({sum_of_weights:.5f}) is different from 1! "
               "Please revise your weighting scheme.")
        raise PyvolcansError(msg)

    return args_dict


def calculate_weighted_analogy_matrix(my_volcano, weights,
                                      analogies=ANALOGY_MATRIX):
    """
    [TEXT TO BE UPDATED]
    Input is dictionary of weights
    e.g. {‘tectonic_setting’: 0.5, ‘geochemistry’: 0.5}
    returns numpy array of weighted matrix.
    NB. We load all the matrices here inside the function
    """
    # get the index for my_volcano
    volcano_idx = convert_to_idx(my_volcano)
       
    weighted_tectonic_analogy = \
        weights['tectonic_setting'] * analogies['tectonic_setting']

    weighted_geochemistry_analogy = \
        weights['geochemistry'] * analogies['geochemistry']

    weighted_morphology_analogy = \
        weights['morphology'] * analogies['morphology']

    weighted_eruption_size_analogy = \
        weights['eruption_size'] * analogies['eruption_size']

    weighted_eruption_style_analogy = \
        weights['eruption_style'] * analogies['eruption_style']

    weighted_total_analogy_matrix = weighted_tectonic_analogy + \
        weighted_geochemistry_analogy + weighted_morphology_analogy + \
        weighted_eruption_size_analogy + weighted_eruption_style_analogy

    #print(weighted_total_analogy_matrix.shape)
    volcans_result = VOLCANO_NAMES.copy()
    volcans_result.columns = ['name', 'country', 'smithsonian_id']
    volcans_result['total_analogy'] = \
        weighted_total_analogy_matrix[volcano_idx,]
    volcans_result['ATs'] = \
        weighted_tectonic_analogy[volcano_idx,]
    volcans_result['AG'] = \
        weighted_geochemistry_analogy[volcano_idx,]
    volcans_result['AM'] = \
        weighted_morphology_analogy[volcano_idx,]
    volcans_result['ASz'] = \
        weighted_eruption_size_analogy[volcano_idx,]
    volcans_result['ASt'] = \
        weighted_eruption_style_analogy[volcano_idx,]

    return volcans_result


def get_analogies(my_volcano, volcans_result, count=10):
    """
    Returns, on screen, the names of the top <count> analogues to
    the target volcano (i.e. my_volcano) and their multi-criteria
    analogy values, as a variable: total_analogy.
    Default <count> = 10.
    """

    # get the index for my_volcano
    volcano_idx = convert_to_idx(my_volcano)
    # calculate the <count> highest values of multi-criteria analogy
    # getting the row corresponding to the target volcano ('my_volcano')
    my_volcano_analogies = volcans_result['total_analogy']
    # getting the indices corresponding to the highest values of analogy
    # in descending order (highest analogy first)
    top_idx = my_volcano_analogies.argsort().tail(count+1)[::-1] #TOP ANALOGUE IS LIKELY TO BE THE TARGET VOLCANO!
    result = volcans_result.iloc[top_idx]
    #probably need a warning message around here, to alert the user if the
    #boolean values below are all 'False', which in short means that the target
    #volcano is not inside the Top 'count' analogues. This would hint to data
    #deficiencies for the target volcano
    my_volcano_boolean_indexes = result.index.isin([volcano_idx])
    filtered_result = result[~my_volcano_boolean_indexes]
    # anywhere 'volcano_idx' came from, make it a str
    volcano_name = get_volcano_name_from_idx(volcano_idx)

    return filtered_result, volcano_name


def check_for_perfect_analogues(result):
    """
    This function takes the main result from running PyVOLCANS
    and assesses whether all the top analogue volcanoes share
    the same value of total analogy, in which case, the user
    might suspect that there are either issues with the data
    or with the weighting scheme (e.g. too simplified) used.
    """
    maximum_analogy=result['total_analogy'].iloc[0]
    if result['total_analogy'].eq(maximum_analogy).all():
        msg = ("WARNING!!! "
               "All top analogue volcanoes have the same value "
               "of total analogy. Please be aware of possible "
               "data deficiencies and/or the use of a simplified "
               "weighting scheme (see Tierz et al., 2019 for more "
               "details).\n")
        raise PyvolcansError(msg)


def open_gvp_website(top_analogue_vnum):
    """
    This function takes a list of indices for the top analogue
    volcanoes to the target volcano (given the weighting scheme
    specified by the user) and opens the Global Volcanism Program
    (GVP) website for the top analogue volcano.
    """
    my_web = f'https://volcano.si.edu/volcano.cfm?vn={top_analogue_vnum}' \
              '&vtab=GeneralInfo'  # Getting to open the General Info tab
    browser_opened = webbrowser.open(my_web)

    if not browser_opened:
        msg = f"No suitable browser to open {my_web}"
        raise PyvolcansError(msg)


def output_result(verbose, my_volcano, result, to_file=None, filename=None):
    """
    TO DO!
    channel: string that specifies whether the writing is to be made onto
             the standard output or to a csv file. Available options: 'stdout'
             and 'csv'
    verbose: true/false to control whether only total analogy or total and
             single-criterion analogies are given as output
    """
    # just adding the same line but outputting the list to a file [IMPROVE]
    # NB. {count - 1} because 'count' includes the target volcano!
    # processing the volcano name to make it more 'machine-friendly'
    
    if verbose:
        my_columns = ['name', 'country', 'smithsonian_id', 'total_analogy',
                      'ATs', 'AG', 'AM', 'ASz', 'ASt']
    else:
        my_columns = ['name', 'country', 'smithsonian_id', 'total_analogy']

    if to_file == 'csv':
        result.to_csv(filename, sep=',', float_format='%.5f',
                      header=True, index=False, columns=my_columns)

    result = result[my_columns].to_string(index=False)

    return result


def match_name(volcano_name):
    """Attempt to match name to Smithsonian catalogue."""
    matched_volcanoes = VOLCANO_NAMES.loc[VOLCANO_NAMES[0] == volcano_name]
    # throw errors whether if volcano does not exist
    # or there are 2+ identical names
    if len(matched_volcanoes) == 0:
        name_suggestions = fuzzy_matching(volcano_name)
        msg = (f"{volcano_name} not found! Did you mean:\n{name_suggestions}")
        raise PyvolcansError(msg)

    if len(matched_volcanoes) > 1:
        name_suggestions = fuzzy_matching(volcano_name)
        msg = (f"Volcano name {volcano_name} is not unique. "
               f"Please provide smithsonian id instead of name.\n{name_suggestions}")
        raise PyvolcansError(msg)

    return matched_volcanoes


def get_analogy_percentile(my_volcano, apriori_volcano,
                           volcans_result):
    """
    [TEXT TO UPDATE!]
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
    # convert volcano names into inds to access the weighted_analogy_matrix
    volcano_idx = convert_to_idx(my_volcano)
    apriori_volcano_idx = convert_to_idx(apriori_volcano) 
    
    # derive a vector with the analogy values for the target volcano

    # derive a vector with the analogy values for the target volcano
    my_analogy_values = volcans_result['total_analogy']
    # calculate percentiles from 0 to 100 (like in VOLCANS for now)
    analogy_percentiles = np.percentile(my_analogy_values,
                                        np.linspace(0, 100, 101),
                                        interpolation='midpoint')
    # find the closest value to the analogy of the a priori volcano
    # NOTE that this value already represents the percentile (0-100)
    my_percentile = (np.abs(analogy_percentiles - \
                            my_analogy_values[apriori_volcano_idx])).argmin()

    # Possible steps:
    return my_percentile

def get_many_analogy_percentiles(my_volcano, apriori_volcanoes_list,
                                 volcans_result):
    """
    [TEXT TO UPDATE!]
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

    # check a priori volcanoes is a list

    percentile_dictionary = {}
    better_analogues_dictionary = {} # 100-percentile

    # loop over get_analogy_percentile
    for volcano in apriori_volcanoes_list:
        percentile = get_analogy_percentile(my_volcano, volcano,
                                            volcans_result)
        percentile_dictionary[volcano] = percentile
        better_analogues_dictionary[volcano] = 100 - percentile

    # adding a 'printing functionality' to the function
    my_volcano_to_print = \
        VOLCANO_NAMES.loc[convert_to_idx(my_volcano)][0]
    print('\n\nAccording to PyVOLCANS, the following percentage of volcanoes in'
          + f' the GVP database\nare better analogues to {my_volcano_to_print}'
          + f' than the \'a priori\' analogues reported below:\n')
    
    for volcano, percentage in better_analogues_dictionary.items():
        if isinstance(volcano, int):
            volcano_idx_to_print = get_volcano_idx_from_number(volcano)
            name_to_print = \
                VOLCANO_NAMES.loc[volcano_idx_to_print][0]
        else:
            volcano_idx_to_print = get_volcano_idx_from_name(volcano)
            name_to_print = volcano

        vnum_to_print = \
                volcans_result['smithsonian_id'].iloc[volcano_idx_to_print]
        print(f'{name_to_print} ({vnum_to_print}): {percentage}%\n')

    return percentile_dictionary, better_analogues_dictionary


class PyvolcansError(Exception):
    """Base class for all PyVOLCANS errors"""
