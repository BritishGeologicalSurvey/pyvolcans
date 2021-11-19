import subprocess
import pytest
import tempfile
import json
from pathlib import Path

@pytest.mark.parametrize("input_args,expected",
        [("--help", "usage: pyvolcans"),
         ("-h", "usage: pyvolcans"),
         ("--version", "v"),
         ("-V", "v"),
         # Odd behaviour with --verbose, half of the output is written to stderr and half to stdout
         ("Hekla --verbose", "ID profile for Hekla, Iceland (372070):"),
         ("Hekla -v", "ID profile for Hekla, Iceland (372070):"),
         ("Hekla --apriori Santorini", "According to PyVOLCANS")])

def test_pyvolcans_output(input_args, expected, capfd):
    subprocess.run(['pyvolcans', *input_args.split()])
    out, err = capfd.readouterr()
    assert expected in out

@pytest.mark.parametrize("input_args,expected",
                         [("-ovd", "Hekla"),
                           ("-oad", "Toasdrfajokull")])
def test_write_files(input_args, expected, tmp_path):
    subprocess.run(['pyvolcans', 'Hekla', '--verbose', input_args], cwd=tmp_path)
    fname = list(Path(tmp_path).glob("*.json"))[0]
    with open(fname) as f:
        # TODO: Test fails because JSON file created by -oad throws a JSONDecodeError
        data = json.load(f)
    assert data[next(iter(data))] == expected
