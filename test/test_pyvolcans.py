# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:49:55 2020

@author: Vyron Christodoulou, John A. Stevenson, Pablo Tierz
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""
import pytest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from pyvolcans.pyvolcans_func import (
    fuzzy_matching,
    match_name,
    get_volcano_idx_from_name,
    get_volcano_name_from_idx,
    get_volcano_number_from_name,
    get_volcano_idx_from_number,
    get_many_analogy_percentiles,
    calculate_weighted_analogy_matrix,
    open_gvp_website,
    plot_bar_apriori_analogues,
    plot_bar_better_analogues,
    set_weights_from_args,
    PyvolcansError
)

# pylint: disable=missing-docstring


def test_volcano_idx():
    idx = get_volcano_idx_from_name(volcano_name='Fuego')
    assert idx == 1071


def test_volcano_name():
    name = get_volcano_name_from_idx(volcano_idx=1071)
    assert name == 'Fuego'


def test_fuzzy_matching():
    volc_matches = fuzzy_matching('West Eifel')
    assert 'West Eifel Volcanic Field' in volc_matches

    # Test with limit
    volc_matches_limit = fuzzy_matching('West Eiffel', limit=3)
    assert 'West Eifel Volcanic Field' in volc_matches_limit


def test_volcano_number():
    number = get_volcano_number_from_name('Santorini')
    assert number == 212040


def test_set_weights_from_args_error():
    args_dict = {'tectonic_setting': 99.00001,
                 'geochemistry': 99.00001,
                 'morphology': 99.00001,
                 'eruption_size': 99.00001,
                 'eruption_style': 99.00001}

    with pytest.raises(PyvolcansError) as exc_info:
        set_weights_from_args(args_dict)

    msg = ("Sum of weights (495.000050000) is different from 1!"
           " Please revise your weighting scheme.")

    assert str(exc_info.value) == msg


@pytest.mark.parametrize("args_dict, expected_weights", [
    ({'tectonic_setting': 0.2,
      'morphology': 0.2,
      'eruption_size': 0.2,
      'geochemistry': 0.2,
      'eruption_style': 0.2}, [0.2, 0.2, 0.2, 0.2, 0.2]),
    ({'tectonic_setting': None,
      'morphology': None,
      'eruption_size': None,
      'geochemistry': None,
      'eruption_style': None}, [0.2, 0.2, 0.2, 0.2, 0.2]),
    ({'tectonic_setting': 1,
      'morphology': None,
      'eruption_size': None,
      'geochemistry': None,
      'eruption_style': None}, [1, 0, 0, 0, 0]),
    ({'tectonic_setting': 0.2,
      'morphology': 0.4,
      'eruption_size': None,
      'geochemistry': 0.2,
      'eruption_style': 0.2}, [0.2, 0.4, 0, 0.2, 0.2])
    ])
def test_set_weights_from_args(args_dict, expected_weights):
    names = list(args_dict.keys())
    result = set_weights_from_args(args_dict)

    assert list(result.keys()) == names
    assert list(result.values()) == expected_weights


def test_volcano_idx_from_number():
    idx = get_volcano_idx_from_number(212040)
    assert idx == 21


@pytest.mark.parametrize("name,expected", [('blah', 'not found'), ('Santa Isabel', 'not unique')])
def test_match_name(name, expected):
    with pytest.raises(PyvolcansError) as excinfo:
        match_name(name)
    assert expected in str(excinfo.value)


@pytest.fixture
def mock_analogies():
    """
    Create mocked analogy matrices for each volcanological criterion.
    Note: The matrix is only one item long so tests must use 'West Eifel
    Volcanic Field' because it is first on the list.
    """
    mock_analogies = {'tectonic_setting': np.array([40000]),
                      'geochemistry': np.array([4000]),
                      'morphology': np.array([400]),
                      'eruption_size': np.array([40]),
                      'eruption_style': np.array([4])}
    return mock_analogies

@pytest.fixture
def mock_weights():
    mock_weights = {'tectonic_setting': 0.2,
                    'geochemistry': 0.2,
                    'morphology': 0.2,
                    'eruption_size': 0.2,
                    'eruption_style': 0.2}
    return mock_weights


def test_plot_bar_apriori_analogues(mock_weights, mock_analogies):
    pandas_df, _ = calculate_weighted_analogy_matrix('West Eifel Volcanic Field',
                                                  mock_weights,
                                                  mock_analogies)
    df_bar = plot_bar_apriori_analogues('West Eifel Volcanic Field',
                                        210010,
                                        ['Hekla'],
                                        pandas_df,
                                        'Test_string')
    df_expected = pd.DataFrame({'name': ['Hekla'], 'ATs': [8000.0],
                                'AG': [800.0], 'AM': [80.0], 'ASz':[8.0],
                                'ASt': [0.8]}, index=[1362])
    assert_frame_equal(df_bar, df_expected)


def test_plot_bar_better_analogues(mock_weights, mock_analogies):
    pandas_df, _ = calculate_weighted_analogy_matrix('West Eifel Volcanic Field',
                                                  mock_weights,
                                                  mock_analogies)
    _, better_analogues = \
        get_many_analogy_percentiles('West Eifel Volcanic Field', ['Hekla'],
                                     pandas_df)

    df_bar = plot_bar_better_analogues('West Eifel Volcanic Field',
                                       210010,
                                       better_analogues,
                                       'Test_string')

    df_expected = pd.DataFrame({'apriori_analogue':['Hekla'],
                                'percentage_better': [100]})
    assert_frame_equal(df_bar, df_expected)


@pytest.mark.parametrize("weights, expected", [
    ({'tectonic_setting': 0,
      'geochemistry': 0.25,
      'morphology': 0.25,
      'eruption_size': 0.25,
      'eruption_style': 0.25}, 1111),
    ({'tectonic_setting': 0.25,
      'geochemistry': 0,
      'morphology': 0.25,
      'eruption_size': 0.25,
      'eruption_style': 0.25}, 10111),
    ({'tectonic_setting': 0.25,
      'geochemistry': 0.25,
      'morphology': 0,
      'eruption_size': 0.25,
      'eruption_style': 0.25}, 11011),
    ({'tectonic_setting': 0.25,
      'geochemistry': 0.25,
      'morphology': 0.25,
      'eruption_size': 0,
      'eruption_style': 0.25}, 11101),
    ({'tectonic_setting': 0.25,
      'geochemistry': 0.25,
      'morphology': 0.25,
      'eruption_size': 0.25,
      'eruption_style': 0}, 11110)])
def test_combined_analogy_matrix_no_tectonic(weights, expected, mock_analogies):
    pandas_df, _ = calculate_weighted_analogy_matrix(
        'West Eifel Volcanic Field', weights, mock_analogies)
    matrix = pandas_df.loc[get_volcano_idx_from_name(
        'West Eifel Volcanic Field'), 'total_analogy']
    assert matrix.astype(int) == expected


def test_open_gvp_website(monkeypatch):
    # Arrange
    def always_false(my_web):
        # This function will replace webbrowser.open and always returns false
        # We have my_web as an argument so our function has the same inputs as
        # webbrowser.open
        return False

    monkeypatch.setattr('pyvolcans.pyvolcans_func.webbrowser.open', always_false)

    # Act
    with pytest.raises(PyvolcansError) as exc_info:
        open_gvp_website(123456)

    # Assert
    msg = "No suitable browser to open https://volcano.si.edu/volcano.cfm?vn=123456&vtab=GeneralInfo"
    assert str(exc_info.value) == msg
