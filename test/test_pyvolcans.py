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


@pytest.fixture
def mock_analogies(monkeypatch):
    monkeypatch.setattr('pyvolcans.load_tectonic_analogy', mock_tectonic_analogy)
    monkeypatch.setattr('pyvolcans.load_eruption_style_analogy', mock_eruption_style_analogy)
    monkeypatch.setattr('pyvolcans.load_eruption_size_analogy', mock_eruption_size_analogy)
    monkeypatch.setattr('pyvolcans.load_geochemistry_analogy', mock_geochemistry_analogy)
    monkeypatch.setattr('pyvolcans.load_morphology_analogy', mock_morphology_analogy)
    

@patch.dict(WEIGHTS, {'tectonic_setting': 0,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_tectonic(mock_analogies):
    matrix = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
 
    assert matrix.astype(int) == 1111


@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_geochem(mock_analogies):
    matrix = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                             tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                             eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                             eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                             morphology_analogy=pyvolcans.load_morphology_analogy(),
                                             geochemistry_analogy=pyvolcans.load_geochemistry_analogy())

    assert matrix.astype(int) == 10111


@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0,
                      'eruption_size': 0.25,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_morphology(mock_analogies):
    matrix = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    assert matrix.astype(int) == 11011



@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0,
                      'eruption_style': 0.25}, clear=True)
def test_calculate_combined_analogy_matrix_no_eruption_size(mock_analogies):
    matrix = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    assert matrix.astype(int) == 11101

@patch.dict(WEIGHTS, {'tectonic_setting':0.25,
                      'geochemistry': 0.25,
                      'morphology': 0.25,
                      'eruption_size': 0.25,
                      'eruption_style': 0}, clear=True)
def test_calculate_combined_analogy_matrix_no_eruption_style(mock_analogies):
    matrix = calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                            tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                            eruption_style_analogy=pyvolcans.load_eruption_style_analogy(),
                                            eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                            morphology_analogy=pyvolcans.load_morphology_analogy(),
                                            geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    assert matrix.astype(int) == 11110


@patch.dict(WEIGHTS, {'tectonic_setting':99,
                      'geochemistry': 99,
                      'morphology': 99,
                      'eruption_size': 99,
                      'eruption_style': 99}, clear=True)
def test_calculate_combined_analogy_matrix_exception_weights_more_than_one(mock_analogies):
    with pytest.raises(PyvolcansError):
        calculate_weighted_analogy_matrix(weights=WEIGHTS,
                                          tectonic_analogy=pyvolcans.load_tectonic_analogy(),
                                          eruption_style_analogy=pyvolcans.load_eruption_style_analogy(), 
                                          eruption_size_analogy=pyvolcans.load_eruption_size_analogy(),
                                          morphology_analogy=pyvolcans.load_morphology_analogy(),
                                          geochemistry_analogy=pyvolcans.load_geochemistry_analogy())
    
