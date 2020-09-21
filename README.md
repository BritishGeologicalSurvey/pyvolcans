# Open-access VOLCANS

Collaborative effort to create an free-software (Python), open-access version of VOLCANS (https://doi.org/10.1007/s00445-019-1336-3). 1st stage: provide the users with results from VOLCANS. 2nd stage: clean, re-test and open the whole VOLCANS code

## Local development setup

In a clean virtual environment, run the following to install dependecies:

```bash
python -m pip install -r requirements.txt
```

Prior to running tests, set the PYTHONPATH to include the project directory:

```bash
export PYTHONPATH=.
```

Run tests with:

```bash
pytest -vs test
```
