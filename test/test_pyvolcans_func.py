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
    format_volcano_name,
    get_volcano_idx_from_name,
    get_volcano_name_from_idx,
    get_volcano_number_from_name,
    get_volcano_idx_from_number,
    get_many_analogy_percentiles,
    get_volcano_source_data,
    get_analogies,
    calculate_weighted_analogy_matrix,
    open_gvp_website,
    plot_bar_apriori_analogues,
    plot_bar_better_analogues,
    set_weights_from_args,
    VOLCANO_NAMES,
    PyvolcansError
)


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


def test_format_volcano_name():
    name = format_volcano_name('Tolima, Nevado del', 351030)
    assert name == 'Tolima_Nevado_del_351030'


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

@pytest.fixture
def mock_result(mock_analogies, mock_weights):
    """
    Create mocked PyVOLCANS result using mocked analogies and weights.
    """
    mock_result = calculate_weighted_analogy_matrix('West Eifel Volcanic Field',
                                                    mock_weights,
                                                    mock_analogies)
    return mock_result


def test_plot_bar_apriori_analogues(mock_result):
    df_bar = plot_bar_apriori_analogues('West Eifel Volcanic Field',
                                        210010,
                                        ['Hekla'],
                                        mock_result,
                                        'Test_string')
    df_expected = pd.DataFrame({'name': ['Hekla'], 'ATs': [8000.0],
                                'AG': [800.0], 'AM': [80.0], 'ASz':[8.0],
                                'ASt': [0.8]}, index=[1362])
    assert_frame_equal(df_bar, df_expected)


def test_plot_bar_better_analogues(mock_result):
    _, better_analogues = \
        get_many_analogy_percentiles('West Eifel Volcanic Field', ['Hekla'],
                                     mock_result)

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
    pandas_df = calculate_weighted_analogy_matrix(
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


def test_get_volcano_source_data():
    # Arrange
    expected = {
        'name': 'Hekla',
        'country': 'Iceland',
        'smithsonian_id': 372070,
        'tectonic_setting': {
                0.0: 'Rift Oceanic Crust'
        },
        'geochemistry': {
            'Foidite': 0.,
            'Phonolite': 0.,
            'Trachyte': 0.,
            'Trachyandesite/Basaltic trachyandesite': 0.,
            'Phono-tephrite/Tephri-phonolite': 0.,
            'Tephrite/Basanite/Trachybasalt': 0.,
            'Basalt': 0.25,
            'Andesite': 0.25,
            'Dacite': 0.25,
            'Rhyolite': 0.25,
        },
        'morphology': 0.39473684210526316,
        'eruption_size': {
            'VEI leq 2': 0.26666666666666666,
            'VEI 3': 0.35,
            'VEI 4': 0.2833333333333333,
            'VEI 5': 0.1,
            'VEI 6': 0.,
            'VEI 7': 0.,
            'VEI 8': 0.,
        },
        'eruption_style': {
            'Lava flow and/or fountaining': 0.8769230769230769,
            'Ballistics and tephra': 0.6923076923076923,
            'Phreatic and phreatomagmatic activity': 0.,
            'Water-sediment flows': 0.15384615384615385,
            'Tsunamis': 0.015384615384615385,
            'Pyroclastic density currents': 0.09230769230769231,
            'Edifice collapse/destruction': 0.,
            'Caldera formation': 0.,
        }
    }

    # Action
    source_data = get_volcano_source_data('Hekla')

    # Assert
    assert source_data == expected


@pytest.mark.parametrize('volcano, weights, expected', [
    ('Korath Range',
     {'tectonic_setting': 0.2,
      'geochemistry': 0.2,
      'morphology': 0.2,
      'eruption_size': 0.2,
      'eruption_style': 0.2},
     r'.* morphology .* eruption_size .* eruption_style'),
    ('Korath Range',
     {'tectonic_setting': 0.2,
      'geochemistry': 0.4,
      'morphology': 0,
      'eruption_size': 0.2,
      'eruption_style': 0.2},
     r'.* eruption_size .* eruption_style'),
    ('Korath Range',
     {'tectonic_setting': 0.2,
      'geochemistry': 0.2,
      'morphology': 0,
      'eruption_size': 0,
      'eruption_style': 0.6},
     r'.* eruption_style'),
])
def test_calculate_weighted_analogy_matrix_warnings(volcano, weights, expected):
    """Test that warnings include correct missing criteria,
    based on regular expression match."""
    with pytest.warns(UserWarning, match=expected):
        calculate_weighted_analogy_matrix(volcano, weights)


def test_get_analogies(mock_result):
    # Arrange
    # Further mock the result by replacing mocked analogies by increasingly
    # adding values of analogy to generate a mocked top 10 analogues
    # We start from index 0, 'West Eifel Volcanic Field'
    mocked_top10_idx = list(range(0,11,1))
    for x in mocked_top10_idx:
        mock_result.loc[x,'total_analogy'] = (x+1) * 10000

    mocked_top_names = get_volcano_name_from_idx(mocked_top10_idx)

    # target volcano, West Eifel Volcanic Field, is not expected in the df
    # NOTE that indices and volcano_names are 'flipped-up' because they are
    # ordered from highest to lowest analogy
    mock_top_names_list = list(mocked_top_names[:0:-1])
    partial_df_expected = pd.DataFrame( \
                               {'name': mock_top_names_list,
                                'total_analogy':
                                    [110000.0, 100000.0,90000.0, 80000.0,
                                     70000.0, 60000.0, 50000.0, 40000.0,
                                     30000.0, 20000.0]},
                                 index = list(range(10,0,-1)))

    # Act
    mock_top_analogues, _ = get_analogies('West Eifel Volcanic Field',
                                       mock_result)
    partial_mock_top_analogues = mock_top_analogues[['name', 'total_analogy']]

    # Assert
    assert_frame_equal(partial_mock_top_analogues, partial_df_expected)
