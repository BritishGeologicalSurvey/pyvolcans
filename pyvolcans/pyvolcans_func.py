# -*- coding: utf-8 -*-
"""
Set of functions related to the implementation of PyVOLCANS

Created on Tue Mar  3 09:49:16 2020

@author: Pablo Tierz, John A. Stevenson, Vyron Christodoulou
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""
import warnings
import webbrowser
from fractions import Fraction

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pyvolcans import (load_tectonic_analogy,
                       load_geochemistry_analogy,
                       load_morphology_analogy,
                       load_eruption_size_analogy,
                       load_eruption_style_analogy,
                       load_volcano_names)

# fuzzywuzzy would like to use a sequence matcher provided by the
# Python-Levenshtein package, but this has dependencies that require
# compilation.  When it is not installed, it uses the matcher provided
# by the standard library difflib and raises a warning.  In our case
# it doesn't make much difference so we suppress the warning.
with warnings.catch_warnings():
    warnings.filterwarnings('ignore',
                            message="Using slow pure-python SequenceMatcher.")
    from fuzzywuzzy import fuzz, process

VOLCANO_NAMES = load_volcano_names()

# dictionary of weights for the volcanological criteria
WEIGHTS = {'tectonic_setting': 0.2, 'geochemistry': 0.2,
           'morphology': 0.2, 'eruption_size': 0.2, 'eruption_style': 0.2}

# load all the data from VOLCANS
ANALOGY_MATRIX = {'tectonic_setting': load_tectonic_analogy(),
                  'geochemistry': load_geochemistry_analogy(),
                  'morphology': load_morphology_analogy(),
                  'eruption_size': load_eruption_size_analogy(),
                  'eruption_style': load_eruption_style_analogy()
                  }


def _frac_to_float(value):
    """
    Converts a string of decimal or fractional number (e.g. '0.5' or '1/2')
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

    # check for lists because value is None if not specified
    if isinstance(value, list):
        if len(value) > 1:
            msg = ("Some criterion weights are duplicated! "
                   "Please revise your weighting scheme.")
            raise PyvolcansError(msg)
        value = value[0]

    if value is None:
        value_as_float = None
    else:
        # criterion weight may be given as decimal or fraction
        if '/' in value:
            try:
                numerator, denominator = value.split('/')
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
    """
    Provides a list of volcanoes with names most similar to volcano_name.

    The function serves to handle possible typos in the name provided for the
    target volcano.

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
                              scorer=fuzz.token_sort_ratio)

    match_idx = [item[2] for item in matches]
    volcano_info = \
        VOLCANO_NAMES.iloc[match_idx].rename(columns={0: 'name',
                                                      1: 'country',
                                                      2: 'smithsonian_id'})
    similar_volcano_names = volcano_info.to_string(index=False)

    return similar_volcano_names


def get_volcano_idx_from_number(volcano_number):
    """
    Derives the index of the volcano in the analogy matrices (VOLCANS) from the
    volcano number (VNUM) in the GVP database (www.volcano.si.edu).

    Parameters
    ----------
    volcano_number : int

    Returns
    -------
    volcano_index : int

    Raises
    ------
    PyvolcansError
        If the VNUM introduced does not exist
    """

    volcano_idx = VOLCANO_NAMES.loc[VOLCANO_NAMES[2] == volcano_number]
    if volcano_idx.empty:
        msg = ("Volcano number does not exist. "
               "Please provide a non-zero, positive, six digits number. To check for "
               "existing volcano numbers (VNUM), please visit www.volcano.si.edu")
        raise PyvolcansError(msg)

    volcano_index = volcano_idx.index[0]

    return volcano_index


def get_volcano_idx_from_name(volcano_name):
    """
    Derives the index of the volcano in the analogy matrices (VOLCANS) from the
    volcano name in the GVP database (www.volcano.si.edu).

    Parameters
    ----------
    volcano_name : str

    Returns
    -------
    volcano_index : int

    Raises
    ------
    PyvolcansError
        Via the call to match_name(volcano_name) function, if the volcano
        name cannot be matched to a volcano index
    """

    matched_volcanoes = match_name(volcano_name)
    volcano_index = matched_volcanoes.index[0]

    return volcano_index


def get_volcano_name_from_idx(volcano_idx):
    """
    Derives the the volcano name in the GVP database (www.volcano.si.edu) from
    the index of the volcano in the analogy matrices (VOLCANS).

    Parameters
    ----------
    volcano_idx : int

    Returns
    -------
    volcano_name : str

    Restrictions
    ------
    The function cannot be called with a value greater than 1438 (N - 1, where
    N is the number of Holocene volcanoes in the GVP database, v. 4.6.7)
    """

    volcano_name = \
        VOLCANO_NAMES.iloc[volcano_idx, 0]

    return volcano_name


def get_volcano_number_from_name(volcano_name):
    """
    Derives the volcano number (VNUM) from the volcano name in the GVP database
    (www.volcano.si.edu).

    Parameters
    ----------
    volcano_name : str

    Returns
    -------
    volcano_vnum : int

    Raises
    ------
    PyvolcansError
        Via the call to match_name(volcano_name) function, if the volcano
        name cannot be matched to a volcano number (VNUM)
    """

    matched_volcanoes = match_name(volcano_name)
    volcano_vnum = matched_volcanoes.iloc[0, 2]
    return volcano_vnum


def convert_to_idx(my_volcano):
    """
    Checks whether the volcano input is a string or not, and in either case,
    derives the index of the volcano in the analogy matrices (VOLCANS).

    Parameters
    ----------
    my_volcano : str or int
        Target volcano selected by the user, as volcano name or volcano number

    Returns
    -------
    volcano_idx : int

    Raises
    ------
    PyvolcansError
        Via either the call to get_volcano_idx_from_name(my_volcano) function,
        if the volcano name cannot be matched to a volcano index, or the call
        to get_volcano_idx_from_number(my_volcano), if the volcano number
        (VNUM) cannot be matched to a volcano index
    """

    if isinstance(my_volcano, str):
        volcano_idx = get_volcano_idx_from_name(my_volcano)
    else:
        volcano_idx = get_volcano_idx_from_number(my_volcano)

    return volcano_idx


def set_weights_from_args(args_dict):
    """
    Transforms the set of weights, for volcanological criteria, introduced by
    the user into a set of weights usable by PyVOLCANS.

    Parameters
    ----------
    args_dict : dict
        Set of weights introduced by the user through the command line
        (see PyVOLCANS help and Tierz et al., 2019, for more details on the
        volcanological criteria associated with the weights)

    Returns
    -------
    args_dict : dict
        Set of weights to be used to run PyVOLCANS. If no weights are given by
        the user, the function assigns all weights the same value (0.2) and
        PyVOLCANS is run using an equal-weight weighting scheme.

        If the user specifies the weights for some volcanological criteria but
        not for others, the function assigns zero values to the those weights
        that are unspecified, and PyVOLCANS is run, if the sum of weights
        provided is equal to one.

    Raises
    ------
    PyvolcansError
        If any of the criterion weights provided is a negative value*, as this
        is incompatible with the VOLCANS method. *Please note that a value of
        `-0` is accepted by the program.

        If the sum of weights provided by the user is different from one*, so
        the total analogy computed by PyVOLCANS is not a weighted average of
        the single-criterion analogies (see Tierz et al., 2019, for more
        details). *Numerical precision asserting this equality is 1e-9.
    """

    # check whether any criterion weight has been given by the user
    no_values_set = all(value is None for value in args_dict.values())

    if no_values_set:
        args_dict = dict.fromkeys(args_dict.keys(), 0.2)
        return args_dict

    # check whether the sum of weights provided sums up to 1
    sum_of_weights = 0
    for key, value in args_dict.items():
        if value is None:
            args_dict[key] = 0
        # check whether any of the criterion weights is negative
        elif value < 0:
            msg = ("Some criterion weights are negative values! "
                   "Please revise your weighting scheme.")
            raise PyvolcansError(msg)
        else:
            sum_of_weights += value

    if not np.isclose(sum_of_weights, 1, rtol=0, atol=1e-9):
        msg = (f"Sum of weights ({sum_of_weights:.9f}) is different from 1! "
               "Please revise your weighting scheme.")
        raise PyvolcansError(msg)

    return args_dict


def calculate_weighted_analogy_matrix(my_volcano, weights,
                                      analogies=ANALOGY_MATRIX):
    """
    Derives a matrix of total and single-criterion analogy values between the
    target volcano and any other volcano in the GVP database
    (www.volcano.si.edu), using the weighting scheme selected by the user.

    Parameters
    ----------
    my_volcano : str or int
        Target volcano selected by the user, as volcano name or volcano number
    weights : dict
        Set of weights (weighting scheme) selected by the user to run PyVOLCANS
    analogies: dict (fixed keyword argument)
        Cross-volcano values of single-criterion analogy between any two
        volcanoes listed in the GVP database (v. 4.6.7), for five different
        volcanological criteria (see Tierz et al., 2019, for more details)

    Returns
    -------
    volcans_result : Pandas dataframe
        Total and single-criterion analogy values between the target volcano
        and any volcano listed in the GVP database (v. 4.6.7)

        Please note that the total analogy values are specific to the set of
        weights (or weighting scheme) that is chosen by the user for each
        particular run of PyVOLCANS. A different weighting scheme can generate
        an entirely different set of total analogy values.

    my_volcano_data_dictionary : dict
        Dictionary containing information on whether there is volcanological
        data available (dict_value = 1), or there is not (dict_value = 0); for
        each of the volcanological criteria used by PyVOLCANS, considering the
        specific target volcano chosen by the user to run the program.
    """

    # get the index for my_volcano
    volcano_idx = convert_to_idx(my_volcano)

    # check for volcanological criteria without data for the target volcano
    my_volcano_data_dictionary = {} # empty dictionary
    # NB. If the single-criterion analogy of the target volcano with itself is
    # equal to zero, then there is no data available for that particular
    # volcanological criterion
    for criterion in analogies.keys():
        single_analogies = analogies[criterion]
        my_volcano_single_analogies = single_analogies[volcano_idx]
        # to make tests pass (my_volcano_single_analogies becomes an int32
        # when implementing some of the tests)
        if isinstance(my_volcano_single_analogies, np.ndarray):
            my_volcano_data_dictionary[criterion] = \
                my_volcano_single_analogies[volcano_idx]

    # calculate single-criterion analogy matrices for specific weighting scheme
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

    # calculate total analogy matrix for specific weighting scheme
    weighted_total_analogy_matrix = weighted_tectonic_analogy + \
        weighted_geochemistry_analogy + weighted_morphology_analogy + \
        weighted_eruption_size_analogy + weighted_eruption_style_analogy

    # arrange final result
    volcans_result = VOLCANO_NAMES.copy()
    volcans_result.columns = ['name', 'country', 'smithsonian_id']
    volcans_result['total_analogy'] = \
        weighted_total_analogy_matrix[volcano_idx, ]
    volcans_result['ATs'] = \
        weighted_tectonic_analogy[volcano_idx, ]
    volcans_result['AG'] = \
        weighted_geochemistry_analogy[volcano_idx, ]
    volcans_result['AM'] = \
        weighted_morphology_analogy[volcano_idx, ]
    volcans_result['ASz'] = \
        weighted_eruption_size_analogy[volcano_idx, ]
    volcans_result['ASt'] = \
        weighted_eruption_style_analogy[volcano_idx, ]

    return volcans_result, my_volcano_data_dictionary


def get_analogies(my_volcano, volcans_result, count=10):
    """
    Derives a filtered Pandas dataframe, which contains the total and single-
    criterion analogy values between the target volcano and a given number of
    'top' analogue volcanoes (specified by count).

    Parameters
    ----------
    my_volcano : str or int
        Target volcano selected by the user, as volcano name or volcano number
    volcans_result : Pandas dataframe
        Total and single-criterion analogy values between the target volcano
        and any volcano listed in the GVP database (v. 4.6.7)

        Please note that the total analogy values are specific to the set of
        weights (or weighting scheme) that is chosen by the user for each
        particular run of PyVOLCANS. A different weighting scheme can generate
        an entirely different set of total analogy values.
    count: int, optional
        Number of top analogue volcanoes to derive. Default = 10

    Returns
    -------
    filtered_result: Pandas dataframe
        Sub-set of results from the Pandas dataframe volcans_result,
        thus only including the data for the top analogue volcanoes
        to the target volcano.
    volcano_name: str
        Target volcano's name in the GVP database (www.volcano.si.edu).
        NB. Variable required to derive some of the outputs of PyVOLCANS
        (see 'output_result()' function).
    """

    # get the index for my_volcano
    volcano_idx = convert_to_idx(my_volcano)
    # get the row corresponding to the target volcano ('my_volcano')
    my_volcano_analogies = volcans_result['total_analogy']
    # get the indices corresponding to the highest values of analogy
    # in descending order (highest analogy first)
    # NB. count+1 is used as the top analogue is likely
    #     to be the target volcano itself
    top_idx = my_volcano_analogies.argsort().tail(count+1)[::-1]
    result = volcans_result.iloc[top_idx]
    # 'filter out' the target volcano from the final result
    my_volcano_boolean_indexes = result.index.isin([volcano_idx])
    filtered_result = result[~my_volcano_boolean_indexes]
    # obtain volcano name from volcano_idx as my_volcano could be an int
    volcano_name = get_volcano_name_from_idx(volcano_idx)

    return filtered_result, volcano_name


def check_for_perfect_analogues(result):
    """
    Assesses whether all the calculated top analogue volcanoes share the same
    value of total analogy, and raises a PyvolcansError exception if that is
    the case.

    Parameters
    ----------
    result: Pandas dataframe
        Sub-set of results from the Pandas dataframe volcans_result,
        thus only including the data for the top analogue volcanoes
        to the target volcano.

    Raises
    -------
    PyvolcansError
        If all the top analogue volcanoes have the same value of total analogy.
        This observation may be related to issues with the data available for
        the target volcano (and/or analogue volcanoes), but can also be
        indicative of the fact that the weighting scheme selected is too
        simplified, or not informative enough (e.g. a single-criterion search
        of volcanoes on subduction zones under continental crust will yield
        hundreds of volcanoes that share that same characteristic. Please see
        Tierz et al., 2019, for more details)
    """

    maximum_analogy = result['total_analogy'].iloc[0]
    if result['total_analogy'].eq(maximum_analogy).all():
        msg = ("WARNING!!! "
               "All top analogue volcanoes have the same value "
               "of total analogy. Please be aware of possible "
               "data deficiencies and/or the use of a simplified "
               "weighting scheme (see Tierz et al., 2019, for more "
               "details).\n")
        raise PyvolcansError(msg)


def check_for_criteria_without_data(my_volcano_data, my_volcano_name):
    """
    Assesses whether some volcanological criteria do not have any data for the
    specific target volcano chosen by the user, raising a PyvolcansError
    exception if this is the case, informing the user which are these criteria.

    Parameters
    ----------
    my_volcano_name : str
        Target volcano selected by the user, as volcano name.
    my_volcano_data: dict
        Dictionary containing information on whether there is volcanological
        data available (dict_value = 1), or there is not (dict_value = 0); for
        each of the volcanological criteria used by PyVOLCANS, considering the
        specific target volcano chosen by the user to run the program.

    Raises
    -------
    PyvolcansError
        If one or more volcanological criteria have no data available for the
        selected target volcano.
    """

    # based on:
    # https://thispointer.com/python-how-to-find-keys-by-value-in-dictionary
    my_list_keys = list()
    my_list_items = my_volcano_data.items()
    for item in my_list_items:
        if item[1] == 0:
            my_list_keys.append(item[0])

    # check whether the list is not empty (in other words, there are some
    # volcanological criteria without data)
    if my_list_keys:
        nodata_criteria_text = ', '.join(my_list_keys)
        msg = ("WARNING!!! "
               "The following volcanological criteria do not have "
               "any data available for the selected target volcano "
               f"({my_volcano_name}): {nodata_criteria_text}. Please "
               "consider excluding these criteria from your weighting scheme "
               "(i.e. setting their weights to zero).")
        raise PyvolcansError(msg)


def open_gvp_website(top_analogue_vnum):
    """
    Opens the GVP website for the top analogue volcano to the target volcano
    identified by PyVOLCANS using the specific weighting scheme selected by
    the user.

    Parameters
    ----------
    top_analogue_vnum: int
        Volcano number (VNUM) of the top analogue volcano. It is used to define
        the URL to open. Please note that the top analogue volcano identified
        by PyVOLCANS is not only dependent on the target volcano, but also on
        the weighting scheme selected to run PyVOLCANS. Different choices of
        weighting scheme may yield different top analogue volcanoes.

    Raises
    -------
    PyvolcansError
        If a web browser to open the URL cannot be identified
    """

    my_web = f'https://volcano.si.edu/volcano.cfm?vn={top_analogue_vnum}' \
        '&vtab=GeneralInfo'  # Open the General Info tab
    browser_opened = webbrowser.open(my_web)

    if not browser_opened:
        msg = f"No suitable browser to open {my_web}"
        raise PyvolcansError(msg)


def output_result(verbose, my_volcano, result, to_file=None, filename=None):
    """
    Prepares the final PyVOLCANS results to be written either to the standard
    output or to a comma-separated-value (csv) file.

    Parameters
    ----------
    verbose : bool
        Indicates whether the verbose mode has been chosen by the user (True).
        This produces an output that includes the single-criterion analogy
        values, in addition to the total analogy values. If verbose mode is not
        chosen (False), the PyVOLCANS output only contains the total analogy
        values.
    my_volcano : str or int
        Target volcano selected by the user, as volcano name or volcano number
    result: Pandas dataframe
        Sub-set of results from the Pandas dataframe volcans_result,
        thus only including the data for the top analogue volcanoes
        to the target volcano.
    to_file : str, optional
        Keyword argument that indicates whether the PyVOLCANS result has to be
        written onto a csv file (to_file='csv') or not (Default, to_file=None)
    filename : str, optional
        Keyword argument that indicates the filename to use for the optional
        csv file containing the PyVOLCANS result. Default filename=None.
        Note that, if 'filename' is specified but 'to_file=None', the variable
        'filename' is not used.

    Returns
    -------
    result: Pandas dataframe
        Sub-set of results from the Pandas dataframe volcans_result, including
        either the total analogy values only or the total and single-criterion
        analogy values, for the top analogue volcanoes to the target volcano,
        given the selected weighting scheme.
    """

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
    """
    Attempts to match the volcano name provided by the user to an existing
    volcano name in the GVP database (www.volcano.si.edu), and provides a list
    of alternatives (via 'fuzzy_matching()') if a unique name cannot be found.

    Parameters
    ----------
    volcano_name : str
        Name of volcano introduced by the user (i.e. target volcano)

    Returns
    -------
    matched_volcanoes : Pandas dataframe
        Contains volcano data for the unique match for the volcano name
        provided (volcano_name)

    Raises
    ------
    PyvolcansError
        If the volcano name does not exist in the GVP database. It gives a list
        of similar volcano names, using fuzzy_matching(volcano_name), before
        raising the exception.

        If the volcano name exists in the GVP database, but it is not a unique
        volcano name. That is: more than one volcano in the database has the
        same name. In this case, it also gives a list of similar volcano names,
        using fuzzy_matching(volcano_name), before raising the exception.
    """

    matched_volcanoes = VOLCANO_NAMES.loc[VOLCANO_NAMES[0] == volcano_name]
    # throw errors either if volcano name does not exist
    if len(matched_volcanoes) == 0:
        name_suggestions = fuzzy_matching(volcano_name)
        msg = (f"{volcano_name} not found! Did you mean:\n{name_suggestions}")
        raise PyvolcansError(msg)

    # or if there are 2+ identical volcano names
    if len(matched_volcanoes) > 1:
        name_suggestions = fuzzy_matching(volcano_name)
        msg = (f"Volcano name {volcano_name} is not unique. "
               f"Please provide smithsonian id instead of name.\n{name_suggestions}")
        raise PyvolcansError(msg)

    return matched_volcanoes


def plot_bar_apriori_analogues(my_volcano_name, my_volcano_vnum,
                               my_apriori_analogues, volcans_result,
                               criteria_weights_text, save_figure=None):
    """
    Plots values of single-criterion and total analogy between the target
    volcano and any a priori analogue provided by the user. It optionally
    saves the figure in png format (600 dpi resolution).

    Parameters
    ----------
    my_volcano_name : str
        Name of volcano introduced by the user (i.e. target volcano).
    my_volcano_vnum: int
        Volcano number (VNUM) of volcano introduced by the user in the
        GVP database (www.volcano.si.edu).
    my_apriori_analogues:
        List of a priori analogues as introduced by the user via the command
        line.
    volcans_result : Pandas dataframe
        Total and single-criterion analogy values between the target volcano
        and any volcano listed in the GVP database (v. 4.6.7).
    criteria_weights_text : str
        Single string indicating the weighting scheme selected by the user.
    save_figure : bool, optional
        Keyword argument that indicates whether the generated figures are to
        be saved in the current working directory, as indicated by the optional
        flag `--save_figure` chosen by the user when running PyVOLCANS.

    Returns
    -------
    all_my_apriori_analogies : Pandas dataframe
        Single-criterion analogy values between the target volcano and all the
        a priori analogues selected by the user. Returned basically for testing
        purposes on the function.
    """

    # derive the indices for all a priori analogues
    my_apriori_volcano_idx = [convert_to_idx(x) for x in my_apriori_analogues]

    # slice volcans_result to derive a data frame with the a priori analogues
    all_my_apriori_analogies = \
        volcans_result.loc[my_apriori_volcano_idx,
                          ['name','ATs','AG','AM','ASz','ASt']]

    # plot single- and total-analogy values for all a priori analogues
    my_apriori_analogues_plot = \
        all_my_apriori_analogies.plot.bar(x="name",
                                          y=["ATs","AG","AM","ASz","ASt"],
                                          stacked=True)

    fig1 = plt.gcf()
    my_apriori_analogues_plot.set_ylim([0,1])
    plt.title(f"A priori analogues: {my_volcano_name} ({my_volcano_vnum})",
              y=1.15, pad=5)
    plt.xlabel(None)
    plt.ylabel('Total Analogy')
    plt.legend(bbox_to_anchor=(0.9, 1.16), ncol=5)
    plt.tight_layout() # ensuring labels/titles are displayed properly

    if save_figure:
        fig1.savefig(
                (f"{my_volcano_name}_apriori_analogues_"
                 f"{criteria_weights_text}.png"),
                dpi=600)

    return all_my_apriori_analogies

def plot_bar_better_analogues(my_volcano_name, my_volcano_vnum,
                              better_analogues, criteria_weights_text,
                              save_figure=None):
    """
    Plots the percentage of 'better analogues' (i.e. higher value of total
    analogy with the target volcano) for each of the a priori analogues
    provided by the user. It optionally saves the figure in png format
    (600 dpi resolution).

    Parameters
    ----------
    my_volcano_name : str
        Name of volcano introduced by the user (i.e. target volcano).
    my_volcano_vnum: int
        Volcano number (VNUM) of volcano introduced by the user in the
        GVP database (www.volcano.si.edu).
    better_analogues: dict
        Dictionary containing the volcano name and percentage* of 'better
        analogues' for all the a priori analogues provided by the user.
        *Percentage is calculated as (100 - Percentile) and represents the
        proportion of volcanoes in the GVP database that are classified as
        'better analogues' (i.e. higher total analogy) by PyVOLCANS (please
        see Tierz et al., 2019, and documentation of the function:
        `get_many_analogy_percentiles()` for more details).
    criteria_weights_text : str
        Single string indicating the weighting scheme selected by the user.
    save_figure : bool, optional
        Keyword argument that indicates whether the generated figures are to
        be saved in the current working directory, as indicated by the optional
        flag `--save_figure` chosen by the user when running PyVOLCANS.

    Returns
    -------
    df_better_analogues : Pandas dataframe
        Values of percentage of 'better analogues' than each of the a priori
        analogues selected, for the specific target volcano. Returned basically
        for testing purposes on the function.
    """
    # open figure for the 'better analogues' bar plot
    # dict to pandas df based on:
    # https://stackoverflow.com/questions/18837262/convert-python-dict-into-a-dataframe
    df_better_analogues = pd.DataFrame(better_analogues.items(),
                                       columns=['apriori_analogue',
                                                'percentage_better'])

    df_better_analogues.plot.bar(x="apriori_analogue",
                                 y="percentage_better",
                                 legend=False,
                                 title=f"Better analogues: {my_volcano_name} ({my_volcano_vnum})",
                                 ylim=[0,50])
    plt.xlabel(None)
    plt.ylabel('Percentage of better analogues')
    plt.tight_layout()
    if save_figure:
        plt.savefig(
                (f"{my_volcano_name}_better_analogues_"
                 f"{criteria_weights_text}.png"),
                 dpi=600)

    return df_better_analogues


def get_analogy_percentile(my_volcano, apriori_volcano,
                           volcans_result):
    """
    Takes the target volcano and another volcano (an 'a priori analogue'), and
    calculates the percentile that the total analogy between the two volcanoes
    represents within the whole distribution of total analogy values between
    the target volcano and all the other volcanoes in the GVP database is
    considered (please see Tierz et al., 2019, for more details).

    Parameters
    ----------
    my_volcano : str or int
        Target volcano selected by the user, as volcano name or volcano number
    apriori_volcano : str or int
        A volcano that is considered, a priori (i.e. by other means different
        from running PyVOLCANS), as a good analogue volcano to the selected
        target volcano
    volcans_result : Pandas dataframe
        Total and single-criterion analogy values between the target volcano
        and any volcano listed in the GVP database (v. 4.6.7)

        Please note that the total analogy values are specific to the set of
        weights (or weighting scheme) that is chosen by the user for each
        particular run of PyVOLCANS. A different weighting scheme can generate
        an entirely different set of total analogy values.

    Returns
    -------
    my_percentile : int
        Percentile that the total analogy value between the a priori analogue
        and the target volcano represents within the distribution of total
        analogy values between the target volcanoes and all the volcanoes in
        the GVP database. Please note that (100 - my_percentile) represents the
        percentage of volcanoes in the GVP database that have higher values of
        total analogy with the target volcano, compared to the a priori
        analogue provided. These volcanoes are interpreted as 'better analogues'
        to the target volcano than the a priori analogue (please see Tierz et
        al., 2019, for more details).

        Please also note that the total analogy values, hence the percentiles
        calculated, are specific to the set of weights (or weighting scheme)
        that is chosen by the user for each particular run of PyVOLCANS.
        A different weighting scheme can generate an entirely different set
        of total analogy values, and hence, of percentile values.
    """

    # convert volcano names into indices to access the weighted_analogy_matrix
    apriori_volcano_idx = convert_to_idx(apriori_volcano)

    # derive a vector with the analogy values for the target volcano
    my_analogy_values = volcans_result['total_analogy']
    # calculate percentiles from 0 to 100 (same method as in VOLCANS currently)
    analogy_percentiles = np.percentile(my_analogy_values,
                                        np.linspace(0, 100, 101),
                                        interpolation='midpoint')
    # find the closest value to the analogy of the a priori volcano
    # NOTE that this value already represents the percentile (0-100)
    my_percentile = (np.abs(analogy_percentiles -
                            my_analogy_values[apriori_volcano_idx])).argmin()

    return my_percentile


def get_many_analogy_percentiles(my_volcano, apriori_volcanoes_list,
                                 volcans_result):
    """
    Iteratively calls 'get_analogy_percentile()' function to derive a
    dictionary of 'a priori analogues' with their corresponding value of
    percentage of 'better analogues' (to the target volcano) that exist in
    the GVP database (www.volcano.si.edu). NB. 'better analogue' means that
    the particular volcano has a higher value of total analogy than the a
    priori analogue, for the specific weighting scheme selected by the user
    (please see Tierz et al., 2019, for more details)

    Parameters
    ----------
    my_volcano : str or int
        Target volcano selected by the user, as volcano name or volcano number
    apriori_volcanoes_list : list
        List of a priori analogues as introduced by the user via the command
        line
    volcans_result : Pandas dataframe
        Total and single-criterion analogy values between the target volcano
        and any volcano listed in the GVP database (v. 4.6.7)

        Please note that the total analogy values are specific to the set of
        weights (or weighting scheme) that is chosen by the user for each
        particular run of PyVOLCANS. A different weighting scheme can generate
        an entirely different set of total analogy values.

    Returns
    -------
    percentile_dictionary : dict
        Dictionary containing the volcano name and percentile* for all the
        a priori analogues provided by the user. *Percentile that the total
        analogy value between the a priori analogue and the target volcano
        represents within the distribution of total analogy values between the
        target volcanoes and all the volcanoes in the GVP database.

    better_analogues_dictionary: dict
        Dictionary containing the volcano name and percentage* of 'better
        analogues' for all the a priori analogues provided by the user.
        *Percentage is calculated as (100 - Percentile) and represents the
        proportion of volcanoes in the GVP database that are classified as
        'better analogues' (i.e. higher total analogy) by PyVOLCANS (please
        see Tierz et al., 2019, for more details).

        Please also note that the total analogy values, hence the percentiles,
        hence the percentages of 'better analogues' calculated are specific to
        the set of weights (or weighting scheme) that is chosen by the user for
        each particular run of PyVOLCANS.
        A different weighting scheme can generate an entirely different set
        of total analogy values, hence of percentile values, and hence of
        percentages of 'better analogues' (please see Tierz et al., 2019, for
        examples of this).
    """

    # create empty dictionaries for percentiles
    # and percentage of better analogues
    percentile_dictionary = {}
    better_analogues_dictionary = {}  # 100-percentile

    # loop over get_analogy_percentile
    for volcano in apriori_volcanoes_list:
        percentile = get_analogy_percentile(my_volcano, volcano,
                                            volcans_result)
        percentile_dictionary[volcano] = percentile
        better_analogues_dictionary[volcano] = 100 - percentile

    # print the percentage of better analogues for each a priori analogue
    my_volcano_to_print = \
        VOLCANO_NAMES.loc[convert_to_idx(my_volcano)][0]
    print('\n\nAccording to PyVOLCANS, the following percentage of volcanoes in'
          + f' the GVP database\nare better analogues to {my_volcano_to_print}'
          + ' than the \'a priori\' analogues reported below:\n')

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
