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
    find_optimal_weights,
    _weighting_scheme_space,
    _mean_rank_of_analogues,
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


# 'a priori' analogue volcanoes to Hekla, Iceland
HEKLA_APRIORI = ['Katla', 'Torfajokull', 'Askja', 'Eyjafjallajokull',
                 'Oraefajokull', 'Krafla', 'Alcedo']

CRITERIA = ['tectonic_setting', 'geochemistry', 'morphology',
            'eruption_size', 'eruption_style']


def test_weighting_scheme_space_sums_to_one():
    schemes = _weighting_scheme_space(grid_step=0.05,
                                      number_of_criteria=5)
    assert np.allclose(schemes.sum(axis=1), 1)


def test_weighting_scheme_space_is_non_negative():
    schemes = _weighting_scheme_space(grid_step=0.05,
                                      number_of_criteria=5)
    assert (schemes >= 0).all()


def test_weighting_scheme_space_size():
    # number of ways to distribute 20 increments across 5 criteria
    schemes = _weighting_scheme_space(grid_step=0.05,
                                      number_of_criteria=5)
    assert schemes.shape == (10626, 5)


def test_weighting_scheme_space_includes_equal_weights():
    schemes = _weighting_scheme_space(grid_step=0.05,
                                      number_of_criteria=5)
    assert np.isclose(schemes, 0.2).all(axis=1).sum() == 1


def test_total_analogy_is_linear_in_the_weights():
    """
    The derivation of optimal weighting schemes relies on the total analogy
    being a weighted average of the single-criterion analogies (please see
    equation 1 in Tierz et al., 2019), and hence a linear function of the
    criterion weights.
    """
    weights = {'tectonic_setting': 0.15, 'geochemistry': 0.40,
               'morphology': 0.10, 'eruption_size': 0.15,
               'eruption_style': 0.20}
    volcans_result = calculate_weighted_analogy_matrix('Hekla', weights)

    single_criterion_analogies = \
        np.column_stack([volcans_result[column] / weight for column, weight
                         in zip(['ATs', 'AG', 'AM', 'ASz', 'ASt'],
                                weights.values())])
    total_analogies = \
        single_criterion_analogies @ np.array(list(weights.values()))

    assert np.allclose(total_analogies, volcans_result['total_analogy'])


def test_mean_rank_of_analogues():
    """
    Two volcanoes, and two weighting schemes that each rank one of them
    first and the other one second.
    """
    single_criterion_analogies = np.array([[1.0, 0.0],
                                           [0.0, 1.0]])
    weighting_schemes = np.array([[1.0, 0.0],
                                  [0.0, 1.0]])

    mean_ranks = _mean_rank_of_analogues(single_criterion_analogies,
                                         weighting_schemes,
                                         apriori_idx=[0])

    assert np.allclose(mean_ranks, [1, 2])


def test_mean_rank_of_analogues_is_chunk_independent():
    rng = np.random.default_rng(42)
    single_criterion_analogies = rng.random((60, 5))
    weighting_schemes = _weighting_scheme_space(grid_step=0.2,
                                                number_of_criteria=5)

    mean_ranks_one_chunk = \
        _mean_rank_of_analogues(single_criterion_analogies,
                                weighting_schemes, [1, 2, 3],
                                chunk_size=10000)
    mean_ranks_many_chunks = \
        _mean_rank_of_analogues(single_criterion_analogies,
                                weighting_schemes, [1, 2, 3],
                                chunk_size=7)

    assert np.allclose(mean_ranks_one_chunk, mean_ranks_many_chunks)


def test_find_optimal_weights_returns_a_weighting_scheme():
    [optimal_weights, _, _, volcano_name] = \
        find_optimal_weights('Hekla', HEKLA_APRIORI)

    assert volcano_name == 'Hekla'
    assert list(optimal_weights.keys()) == CRITERIA
    assert np.isclose(sum(optimal_weights.values()), 1)
    assert all(weight >= 0 for weight in optimal_weights.values())


def test_find_optimal_weights_beats_equal_weights():
    """
    The optimal weighting scheme must rank the 'a priori' analogue volcanoes
    at least as highly as the equal-weight weighting scheme does, because the
    latter is one of the candidate weighting schemes.
    """
    [_, optimal_mean_rank, _, _] = \
        find_optimal_weights('Hekla', HEKLA_APRIORI)

    equal_weights = dict.fromkeys(CRITERIA, 0.2)
    volcans_result = calculate_weighted_analogy_matrix('Hekla', equal_weights)
    ranks = volcans_result['total_analogy'].rank(ascending=False,
                                                 method='min')
    apriori_idx = [get_volcano_idx_from_name(volcano) for volcano
                   in HEKLA_APRIORI]
    equal_weights_mean_rank = ranks.iloc[apriori_idx].mean()

    assert optimal_mean_rank <= equal_weights_mean_rank


def test_find_optimal_weights_recovers_a_known_weighting_scheme():
    """
    The top analogue volcanoes for a given weighting scheme should be
    explained by a weighting scheme that emphasises the same volcanological
    criterion.
    """
    geochemistry_weights = {'tectonic_setting': 0.05, 'geochemistry': 0.80,
                            'morphology': 0.05, 'eruption_size': 0.05,
                            'eruption_style': 0.05}
    volcans_result = calculate_weighted_analogy_matrix('Hekla',
                                                       geochemistry_weights)
    top_analogues = \
        volcans_result.drop(index=get_volcano_idx_from_name('Hekla')) \
                      .nlargest(8, 'total_analogy')['name'].tolist()

    [optimal_weights, _, _, _] = find_optimal_weights('Hekla', top_analogues)

    assert optimal_weights['geochemistry'] == \
        max(optimal_weights.values())


def test_find_optimal_weights_near_optimal_region():
    [optimal_weights, _, near_optimal_region, _] = \
        find_optimal_weights('Hekla', HEKLA_APRIORI)

    assert near_optimal_region.index.name == 'criterion'
    assert list(near_optimal_region.index) == CRITERIA
    assert (near_optimal_region['weight_min'] <=
            near_optimal_region['weight_median']).all()
    assert (near_optimal_region['weight_median'] <=
            near_optimal_region['weight_max']).all()
    # the optimal weighting scheme is itself one of the near-optimal schemes
    for criterion, weight in optimal_weights.items():
        assert near_optimal_region.loc[criterion, 'weight_min'] <= weight
        assert weight <= near_optimal_region.loc[criterion, 'weight_max']


def test_find_optimal_weights_near_optimal_proportion():
    """
    The number of near-optimal weighting schemes should be close to the
    requested proportion of the weighting schemes explored. It is not exactly
    equal to it because many weighting schemes share the same mean rank.
    """
    number_of_schemes = len(_weighting_scheme_space(grid_step=0.05,
                                                    number_of_criteria=5))

    for proportion in [0.05, 0.10, 0.25]:
        [_, _, near_optimal_region, _] = \
            find_optimal_weights('Hekla', HEKLA_APRIORI,
                                 near_optimal_proportion=proportion)
        actual_proportion = \
            near_optimal_region.attrs['number_of_schemes'] / number_of_schemes

        assert abs(actual_proportion - proportion) < 0.02


def test_find_optimal_weights_near_optimal_region_attributes():
    [_, optimal_mean_rank, near_optimal_region, _] = \
        find_optimal_weights('Hekla', HEKLA_APRIORI)

    minimum_mean_rank, maximum_mean_rank = \
        near_optimal_region.attrs['mean_rank_range']

    assert near_optimal_region.attrs['number_of_schemes'] > 0
    assert np.isclose(minimum_mean_rank, optimal_mean_rank)
    assert minimum_mean_rank <= maximum_mean_rank


def test_find_optimal_weights_wider_proportion_is_nested():
    """
    Widening the proportion of near-optimal weighting schemes cannot narrow
    the range of weights taken by any volcanological criterion.
    """
    [_, _, narrow_region, _] = \
        find_optimal_weights('Hekla', HEKLA_APRIORI,
                             near_optimal_proportion=0.05)
    [_, _, wide_region, _] = \
        find_optimal_weights('Hekla', HEKLA_APRIORI,
                             near_optimal_proportion=0.25)

    assert (wide_region['weight_min'] <= narrow_region['weight_min']).all()
    assert (wide_region['weight_max'] >= narrow_region['weight_max']).all()


@pytest.mark.parametrize("near_optimal_proportion", [0, -0.1, 1.5])
def test_find_optimal_weights_invalid_proportion(near_optimal_proportion):
    with pytest.raises(PyvolcansError, match="must range between 0 and 1"):
        find_optimal_weights(
            'Hekla', HEKLA_APRIORI,
            near_optimal_proportion=near_optimal_proportion)


def test_find_optimal_weights_excludes_target_volcano():
    """
    A volcano is a perfect analogue to itself, and must not be ranked among
    its own analogue volcanoes.
    """
    [_, optimal_mean_rank, _, _] = find_optimal_weights('Hekla', ['Katla'])

    assert optimal_mean_rank >= 1


def test_find_optimal_weights_warns_on_few_apriori_volcanoes():
    with pytest.warns(UserWarning, match="unlikely to be well constrained"):
        find_optimal_weights('Hekla', ['Katla', 'Askja'])


def test_find_optimal_weights_no_apriori_volcanoes():
    with pytest.raises(PyvolcansError, match="No 'a priori' analogue volcano"):
        find_optimal_weights('Hekla', [])


@pytest.mark.parametrize("grid_step", [0, -0.05, 1.5, 0.03])
def test_find_optimal_weights_invalid_grid_step(grid_step):
    with pytest.raises(PyvolcansError, match="whole number of intervals"):
        find_optimal_weights('Hekla', HEKLA_APRIORI, grid_step=grid_step)


def test_find_optimal_weights_unknown_volcano():
    with pytest.raises(PyvolcansError, match="not found!"):
        find_optimal_weights('Heklaaa', HEKLA_APRIORI)


def test_find_optimal_weights_unknown_apriori_volcano():
    with pytest.raises(PyvolcansError, match="not found!"):
        find_optimal_weights('Hekla', ['Katla', 'Torfajokulll'])
