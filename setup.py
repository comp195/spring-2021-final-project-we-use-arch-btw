# [metadata]
# name = lvl
# version = 1.0.0

# [options]
# packages = find:
# install_requires = 
#     pygobject
#     fuzzywuzzy
#     python-levenshtein
#     appdirs

# include_package_data = True
from setuptools import setup

setup(
    name='lvl',
    version='1.0.0',
    packages=[
        'LVL',
        'LVL.LocalStorageHandler',
        'LVL.Media',
        'LVL.UI',
        'LVL.UI.bulk_import'
    ],
    install_requires=[
        'pygobject',
        'fuzzywuzzy',
        'python-levenshtein',
        'appdirs'
    ],
    include_package_data = True,
    package_data={
        "": ["*.ui"],
        "LVL.LocalStorageHandler": ["*.png"]
    },
    entry_points = {
        "console_scripts": [
            "lvl=LVL:run_app"
        ]
    }
)