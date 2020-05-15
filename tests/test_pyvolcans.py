# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:49:55 2020

@author: pablo
"""

from pyvolcans_func import get_volcano_idx_from_name, get_volcano_name_from_idx


def test_volcano_idx():
    idx = get_volcano_idx_from_name(volcano_name='West Eifel Volcanic Field')
    assert 0 == idx
    

def test_volcano_name():
    name = get_volcano_name_from_idx(volcano_idx=1071)
    assert 'Fuego' == name