import pytest

from pyvolcans import pyvolcans_func


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
            'VEI ≤ 2': 0.26666666666666666,
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
    source_data = pyvolcans_func.get_volcano_source_data('Hekla')

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
        pyvolcans_func.calculate_weighted_analogy_matrix(volcano, weights)
