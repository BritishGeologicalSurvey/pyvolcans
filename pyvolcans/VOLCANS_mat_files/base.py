"""
Created on Thu Oct 15 12:48:00 2020

@author: Vyron Christodoulou, John A. Stevenson, Pablo Tierz
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""
import pandas as pd
from pathlib import Path
from pymatreader import read_mat

BASE_DIR = Path(__file__).resolve().parent
DIRNAME_ANALOGY = BASE_DIR.joinpath("analogy_mats")
DIRNAME_VOLCANO = BASE_DIR.joinpath("VOTW_prepared_data")


def load_tectonic_analogy():
    return read_mat(DIRNAME_ANALOGY.joinpath("ATfinal_allvolcs.mat"))["AT_allcross"]


def load_geochemistry_analogy():
    return read_mat(DIRNAME_ANALOGY.joinpath("AGfinal_allvolcs_ALU_QUET.mat"))["AG_allcross"]


def load_morphology_analogy():
    return read_mat(DIRNAME_ANALOGY.joinpath("AMfinal_allvolcs_QUET.mat"))["AM_allcross"]


def load_eruption_size_analogy():
    return read_mat(DIRNAME_ANALOGY.joinpath("ASzfinal_allvolcs_SINA.mat"))["ASz_allcross"]


def load_eruption_style_analogy():
    return read_mat(DIRNAME_ANALOGY.joinpath("AStfinal_allvolcs_SINA.mat"))["ASt_allcross"]


def load_volcano_names():
    return pd.read_csv(DIRNAME_VOLCANO.joinpath("volc_names.csv"), header=None)
