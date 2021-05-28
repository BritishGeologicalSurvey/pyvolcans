"""
Setup script for the pyvolcans library
"""
import pathlib
from setuptools import setup
import versioneer

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyvolcans",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A tool for identifying volcano analogues.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BritishGeologicalSurvey/pyvolcans",
    author="BGS Volcanology",
    author_email="pablo@bgs.ac.uk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    packages=["pyvolcans"],
    include_package_data=True,
    install_requires=[
        'fuzzywuzzy',
        'numpy',
        'pandas',
        'pymatreader',
        'matplotlib',
    ],
    extras_require={
        'dev': ['flake8',
                'ipdb',
                'ipython',
                'pytest',
                'pytest-cov',
                'versioneer'
                ]},
    entry_points={
        "console_scripts": [
            "pyvolcans=pyvolcans.pyvolcans:cli",
        ]
    },
)
