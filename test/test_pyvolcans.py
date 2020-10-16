# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:49:55 2020

@author: pablo
"""
import functools
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

def mock_tectonic_analogy():
    return np.array([40000])

def mock_geochemistry_analogy():
    return np.array([4000])

def mock_morphology_analogy():
    return np.array([400])

def mock_eruption_size_analogy():
    return np.array([40])

def mock_eruption_style_analogy():
    return np.array([4])

# Make new decorator
#https://stackoverflow.com/questions/27636897/python-unites-gathering-multiple-patch-decorators-within-another-decorator

def patch_all(func):
    @patch('pyvolcans.load_tectonic_analogy', side_effect=mock_tectonic_analogy)
    @patch('pyvolcans.load_eruption_style_analogy', side_effect=mock_eruption_style_analogy)
    @patch('pyvolcans.load_eruption_size_analogy', side_effect=mock_eruption_size_analogy)
    @patch('pyvolcans.load_geochemistry_analogy', side_effect=mock_geochemistry_analogy)
    @patch('pyvolcans.load_morphology_analogy', side_effect=mock_morphology_analogy)
    @functools.wraps(func)
    def functor(*args, **kwargs):
        return func(*args,  **kwargs)
    return functor

@patch_all
@patch.dict(WEIGHTS, {'tectonic_setting': 0,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_tectonic(*args, **kwargs):
    mat = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
 
    assert mat.astype(int) == 1111

@patch_all
@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_geochem(*args, **kwargs):
    mat = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                             tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                             eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                             eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                             morphology_analogy=pyvolcans.load_morphology_analogy(),
                                             geochemistry_analogy=pyvolcans.load_geochemistry_analogy())

    assert mat.astype(int) == 10111

@patch_all
@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_morphology(*args, **kwargs):
    mat = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    assert mat.astype(int) == 11011



@patch_all
@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_eruption_size(*args, **kwargs):
    mat = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    assert mat.astype(int) == 11101

@patch_all 
@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0}, clear=True)
def test_calculate_combined_analogy_matrix_no_eruption_style(*args, **kwargs):
    mat = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    assert mat.astype(int) == 11110


@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_exception(*args, **kwargs):
    with pytest.raises(PyvolcansError):
        assert calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                                 tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                                 eruption_style_analogy=pyvolcans.load_eruption_style_analogy(), 
                                                 eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                                 morphology_analogy=pyvolcans.load_morphology_analogy(),
                                                 geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    
