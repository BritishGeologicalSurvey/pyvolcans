import os
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from pymatreader import read_mat
import pytest

from pyvolcans import pyvolcans_func as funcs


CRITERIA = [
    'tectonic_setting', 'geochemistry', 'morphology',
    'eruption_size', 'eruption_style',
]
COMPONENTS = ['ATs', 'AG', 'AM', 'ASz', 'ASt']
COLUMNS = ['name', 'country', 'smithsonian_id', 'total_analogy'] + COMPONENTS
TECTONIC_ONLY = dict(zip(CRITERIA, [1.0, 0.0, 0.0, 0.0, 0.0]))
DATA_FILES = [
    ('ATfinal_allvolcs.mat', 'AT_allcross'),
    ('AGfinal_allvolcs_ALU_QUET.mat', 'AG_allcross'),
    ('AMfinal_allvolcs_QUET.mat', 'AM_allcross'),
    ('ASzfinal_allvolcs_SINA.mat', 'ASz_allcross'),
    ('AStfinal_allvolcs_SINA.mat', 'ASt_allcross'),
]


def assert_exact_frame(actual, expected, check_index_type=True):
    assert_frame_equal(actual, expected, check_exact=True,
                       check_index_type=check_index_type, check_column_type=True)
    assert actual.attrs == expected.attrs


@pytest.fixture(scope='module')
def real_hekla_inputs():
    data_dir = Path(funcs.__file__).parent / 'VOLCANS_mat_files'
    names = pd.read_csv(data_dir / 'VOTW_prepared_data' / 'volc_names.csv',
                        header=None)
    names.columns = ['name', 'country', 'smithsonian_id']
    matches = names.index[names['name'].eq('Hekla')].tolist()
    assert len(matches) == 1
    index = matches[0]
    assert names.loc[index, 'smithsonian_id'] == 372070
    assert names.loc[index, 'country'] == 'Iceland'
    rows = {}
    for criterion, (filename, variable) in zip(CRITERIA, DATA_FILES):
        matrix = read_mat(str(data_dir / 'analogy_mats' / filename))[variable]
        assert matrix.shape == (len(names), len(names))
        rows[criterion] = matrix[index].copy()
    return {'names': names, 'target_index': index, 'rows': rows}


def weighted_case(data, weights):
    before_weights = weights.copy()
    actual = funcs.calculate_weighted_analogy_matrix('Hekla', weights)
    assert weights == before_weights
    components = np.stack([weights[k] * data['rows'][k] for k in CRITERIA])
    expected = data['names'].copy()
    expected['total_analogy'] = components.sum(axis=0)
    for column, values in zip(COMPONENTS, components):
        expected[column] = values
    assert actual.columns.tolist() == COLUMNS
    assert_exact_frame(actual.iloc[:, :3], expected.iloc[:, :3])
    assert_frame_equal(actual.iloc[:, 3:], expected.iloc[:, 3:],
                       check_exact=False, check_index_type=True,
                       check_column_type=True, rtol=1e-12, atol=1e-12)
    # Keep the existing full-sort tie order of the current runtime. Tied
    # identities need not be identical across NumPy/pandas versions.
    positions = actual['total_analogy'].argsort().to_numpy()[::-1]
    reference = actual.iloc[positions]
    reference = reference.loc[reference.index != data['target_index']]
    return {'matrix': actual, 'reference': reference,
            'target_index': data['target_index']}


@pytest.fixture(scope='module')
def tied_case(real_hekla_inputs):
    return weighted_case(real_hekla_inputs, TECTONIC_ONLY.copy())


def assert_selection(case, target, count):
    matrix = case['matrix']
    before = matrix.copy(deep=True)
    result, name = funcs.get_analogies(target, matrix, count)
    assert_exact_frame(matrix, before)
    assert name == 'Hekla'
    assert result.columns.tolist() == COLUMNS
    assert case['target_index'] not in result.index
    assert 372070 not in result['smithsonian_id'].tolist()
    assert len(result) == min(count, len(matrix) - 1)
    assert_exact_frame(result, case['reference'].iloc[:count], check_index_type='equiv')


@pytest.mark.parametrize(('target', 'count'), [
    pytest.param('Hekla', 1, id='name-count1'),
    pytest.param('Hekla', 3, id='name-count3'),
    pytest.param(372070, 1, id='number-count1'),
    pytest.param(372070, 3, id='number-count3'),
])
def test_real_tied_analogue_count(tied_case, target, count):
    assert_selection(tied_case, target, count)


def test_real_positive_count_saturates_at_available_analogues(tied_case):
    assert_selection(tied_case, 'Hekla', len(tied_case['matrix']) + 561)


def test_real_equal_weights_default_count_remains_compatible(real_hekla_inputs):
    case = weighted_case(real_hekla_inputs, dict.fromkeys(CRITERIA, 0.2))
    assert_selection(case, 'Hekla', 10)


def table_rows(stdout):
    lines = stdout.splitlines()
    headers = [i for i, line in enumerate(lines)
               if 'smithsonian_id' in line and 'total_analogy' in line]
    assert len(headers) == 1
    return [line for line in lines[headers[0] + 1:] if line.strip()]


@pytest.mark.parametrize('count', [
    pytest.param(1, id='count1'), pytest.param(3, id='count3'),
])
def test_installed_console_real_tied_analogue_rows(tied_case, tmp_path, count):
    executable = Path(sys.executable).parent / (
        'pyvolcans.exe' if os.name == 'nt' else 'pyvolcans')
    assert executable.is_file()
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    env.update(MPLBACKEND='Agg', MPLCONFIGDIR=str(tmp_path / 'mpl-cache'),
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    command = [str(executable), 'Hekla', '-Ts', '1', '--count', str(count)]
    process = subprocess.run(command, cwd=str(tmp_path), env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True, timeout=60)
    assert process.returncode == 0, process.stderr
    assert 'Top {} analogue volcanoes for Hekla'.format(count) in process.stdout
    rows = table_rows(process.stdout)
    assert len(rows) == count
    expected = tied_case['reference'].iloc[:count]
    for line, row in zip(rows, expected.itertuples()):
        pattern = (r'^\s*' + re.escape(row.name) + r'\s+'
                   + re.escape(row.country) + r'\s+'
                   + str(row.smithsonian_id)
                   + r'\s+([-+]?(?:\d+(?:\.\d*)?|\.\d+)'
                     r'(?:[eE][-+]?\d+)?)\s*$')
        match = re.fullmatch(pattern, line)
        assert match is not None, line
        assert float(match.group(1)) == float(row.total_analogy)
    assert not list(tmp_path.glob('*.csv'))
    assert not list(tmp_path.glob('*.json'))
