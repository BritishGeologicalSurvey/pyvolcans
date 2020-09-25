# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:49:55 2020

@author: pablo
"""
from pyvolcans.pyvolcans_func import (
    fuzzy_matching,
    get_volcano_idx_from_name,
    get_volcano_name_from_idx,
    get_volcano_number_from_name
)

# pylint: disable=missing-docstring


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
