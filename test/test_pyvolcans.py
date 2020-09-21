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


def test_volcano_idx():
    idx = get_volcano_idx_from_name(volcano_name='Fuego')
    assert 1071 == idx


def test_volcano_name():
    name = get_volcano_name_from_idx(volcano_idx=1071)
    assert 'Fuego' == name


def test_fuzzy_matching():
    name = fuzzy_matching('West Eifel')
    assert isinstance(name, str)
    name = fuzzy_matching('West Eiffel')
    assert isinstance(name, str)

def test_volcano_number():
    number = get_volcano_number_from_name('Santorini')
    assert 212040 == number
