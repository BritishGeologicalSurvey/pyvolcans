# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:49:55 2020

@author: Vyron Christodoulou, John A. Stevenson, Pablo Tierz  
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""
import pytest
from unittest.mock import patch

import numpy as np

import pyvolcans
from pyvolcans.pyvolcans_func import (
    fuzzy_matching,
    match_name,
    get_volcano_idx_from_name,
    get_volcano_name_from_idx,
    get_volcano_number_from_name,
    get_volcano_idx_from_number,
    calculate_weighted_analogy_matrix,
    set_weights_from_args,
    PyvolcansError
)

from pyvolcans import (load_tectonic_analogy,
                       load_geochemistry_analogy,
                       load_eruption_size_analogy,
                       load_eruption_style_analogy,
                       load_morphology_analogy)

# pylint: disable=missing-docstring



def test_volcano_idx():
    idx = get_volcano_idx_from_name(volcano_name='Fuego')
    assert idx == 1071


def test_volcano_name():
    name = get_volcano_name_from_idx(volcano_idx=1071)
    assert name == 'Fuego'


def test_fuzzy_matching():
    volc_matches = fuzzy_matching('West Eifel')
    assert isinstance(volc_matches, str)
    assert len(volc_matches) == 681
    assert 'West Eifel Volcanic Field' in volc_matches
    volc_matches_limit = fuzzy_matching('West Eiffel', limit=2)
    assert len(volc_matches_limit) == 161
    assert 'West Eifel Volcanic Field' in volc_matches


def test_volcano_number():
    number = get_volcano_number_from_name('Santorini')
    assert number == 212040


def test_set_weights_from_args_error():
    args_dict = {'tectonic_setting': 99,
                 'geochemistry': 99,
                 'morphology': 99,
                 'eruption_size': 99,
                 'eruption_style': 99}

    with pytest.raises(PyvolcansError) as exc_info:
        set_weights_from_args(args_dict)

    assert str(exc_info.value) == "Sum of weights (495) is different from 1!"


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
         matched = match_name(name)
    assert expected in str(excinfo.value)


@pytest.fixture
def analogies():
    analogies = {'tectonic_setting': np.array([40000]), 'geochemistry': np.array([4000]),
                 'morphology': np.array([400]), 'eruption_size': np.array([40]), 'eruption_style': np.array([4])}
    return analogies

@pytest.mark.parametrize("weights,expected",
                        [({'tectonic_setting': 0,
                         'geochemistry': 0.25,
                         'morphology': 0.25,
                         'eruption_size': 0.25,
                         'eruption_style': 0.25}, 1111)])
def test_combined_analogy_matrix_no_tectonic(weights, expected, analogies):
    matrix = calculate_weighted_analogy_matrix(weights, analogies)
    assert matrix.astype(int) == expected


@pytest.mark.parametrize("weights,expected",
                        [({'tectonic_setting': 0.25,
                           'geochemistry': 0,
                           'morphology': 0.25,
                           'eruption_size': 0.25,
                           'eruption_style': 0.25}, 10111)])
def test_combined_analogy_matrix_no_geochemistry(weights, expected, analogies):
    matrix = calculate_weighted_analogy_matrix(weights, analogies)
    assert matrix.astype(int) == expected


@pytest.mark.parametrize("weights,expected", 
                       [({'tectonic_setting':0.25,
                          'geochemistry': 0.25,
                          'morphology': 0,
                          'eruption_size': 0.25,
                          'eruption_style': 0.25}, 11011)])
def test_combined_analogy_matrix_no_morphology(weights, expected, analogies):
    matrix = calculate_weighted_analogy_matrix(weights, analogies)
    assert matrix.astype(int) == expected


@pytest.mark.parametrize("weights,expected",
                        [({'tectonic_setting':0.25,
                           'geochemistry': 0.25,
                           'morphology': 0.25,
                           'eruption_size': 0,
                           'eruption_style': 0.25}, 11101)])

def test_combined_analogy_matrix_no_eruption_size(weights, expected, analogies):
    matrix = calculate_weighted_analogy_matrix(weights, analogies)
    assert matrix.astype(int) == expected

@pytest.mark.parametrize("weights,expected",
                        [({'tectonic_setting':0.25,
                           'geochemistry': 0.25,
                           'morphology': 0.25,
                           'eruption_size': 0.25,
                           'eruption_style': 0}, 11110)])
def test_combined_analogy_matrix_no_eruption_style(weights, expected, analogies):
    matrix = calculate_weighted_analogy_matrix(weights, analogies)
    assert matrix.astype(int) == expected


