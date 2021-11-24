import subprocess
import pytest
import tempfile
import json
import pandas as pd
from pathlib import Path

@pytest.mark.parametrize("input_args,expected",
        [("--help", "usage: pyvolcans"),
         ("-h", "usage: pyvolcans"),
         ("--version", "v"),
         ("-V", "v"),
         # Odd behaviour with --verbose, half of the output is written to stderr and half to stdout
         ("Hekla --verbose", "ID profile for Hekla, Iceland (372070):"),
         ("Hekla -v", "ID profile for Hekla, Iceland (372070):"),
         ("Hekla --apriori Santorini", "According to PyVOLCANS"),
         ("Vesuvius -Ts 1 -v", "'tectonic_setting': 1.0"),
         ("Vesuvius -G 1 -v", "'geochemistry': 1.0"),
         ("Vesuvius -M 1 -v", "'morphology': 1.0"),
         ("Vesuvius -Sz 1 -v", "'eruption_size': 1.0"),
         ("Vesuvius -St 1 -v", "'eruption_style': 1.0"),
         ("Fuego --count 50", "Top 50")])
def test_pyvolcans_output(input_args, expected, capfd):
    subprocess.run(['pyvolcans', *input_args.split()])
    out, err = capfd.readouterr()
    assert (expected in out or expected in err)


@pytest.mark.parametrize("input_args,expected",
                         [("Hekla -ovd", "Hekla"),
                          ("Hekla -oad", "Torfajokull"),
                          ("Fuego -ovd", "Fuego"),
                          ("Fuego -oad", "Klyuchevskoy"),
                          ("Sabancaya -oad", "Peuet Sague")])
def test_write_json_files(input_args, expected, tmp_path):
    subprocess.run(['pyvolcans', '--verbose', *input_args.split()],
                    cwd=tmp_path)
    fname = list(Path(tmp_path).glob("*.json"))[0]
    with open(fname) as f:
        data = json.load(f)
    #`-ovd` returns a dict, `-oad` returns a list of dict
    if type(data) == dict:
        assert data['name'] == expected
    elif type(data) == list:
        top1_analogue = data[0]
        assert top1_analogue['name'] == expected


@pytest.mark.parametrize("input_args,expected",
                         [("Alutu -w", "222040"),
                          ("Vulcano -w", "263310")])
def test_write_csv_files(input_args, expected, tmp_path):
    # Arrange / Action
    subprocess.run(['pyvolcans', '--verbose', *input_args.split()],
                    cwd=tmp_path)
    fname = list(Path(tmp_path).glob("*.csv"))[0]
    data = pd.read_csv(fname)
    top1_analogue = data.iloc[0, ]
    # Assert
    assert top1_analogue['smithsonian_id'] == int(expected)

@pytest.mark.parametrize("input_args,expected",
                         [("Fuego -G 99", "PyVOLCANS: Sum of weights"),
                          ("Fuego -Sz -1", "PyVOLCANS: Some criterion weights")])
def test_pyvolcans_weight_errors(input_args, expected, capfd):
    subprocess.run(['pyvolcans', *input_args.split()])
    _, err = capfd.readouterr()

    assert expected in err