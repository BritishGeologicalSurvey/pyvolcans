# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:49:55 2020

@author: pablo
"""
import pytest
from unittest.mock import patch

import numpy as np

import pyvolcans
from pyvolcans.pyvolcans_func import (
    fuzzy_matching,
    get_volcano_idx_from_name,
    get_volcano_name_from_idx,
    get_volcano_number_from_name,
    calculate_weighted_analogy_matrix,
    PyvolcansError
)

from pyvolcans import (load_tectonic_analogy,
                       load_geochemistry_analogy,
                       load_eruption_size_analogy,
                       load_eruption_style_analogy,
                       load_morphology_analogy)

# pylint: disable=missing-docstring

WEIGHTS = {}


def test_volcano_idx():
    idx = get_volcano_idx_from_name(volcano_name='Fuego')
    assert idx == 1071


def test_volcano_name():
    name = get_volcano_name_from_idx(volcano_idx=1071)
    assert name == 'Fuego'


def test_fuzzy_matching():
    names = fuzzy_matching('West Eifel')
    assert len(names) == 10
    assert 'West Eifel Volcanic Field' in names

    names = fuzzy_matching('West Eiffel', limit=2)
    assert len(names) == 2
    assert 'West Eifel Volcanic Field' in names


def test_volcano_number():
    number = get_volcano_number_from_name('Santorini')
    assert number == 212040


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


@pytest.mark.parametrize("weights,expected",
                       [({'tectonic_setting':99,
                          'geochemistry': 99,
                          'morphology': 99,
                          'eruption_size': 99,
                          'eruption_style': 99}, PyvolcansError)])
def test_combined_analogy_matrix_exception_weights_more_than_one(weights, expected, analogies):
    with pytest.raises(expected):
        calculate_weighted_analogy_matrix(weights, analogies)
                                        
    
