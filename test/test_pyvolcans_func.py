import pytest

from pyvolcans import pyvolcans_func


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
