"""stfc_territories.py - Pull data from https://stfc.space and write to CSV file.

NOTE: This application requires the Requests Module from PyPi. This can
      be installed by running `pip install -U requests`.
NOTE: To access a REST API via https, the Python implementation must be
      compiled with SSL support (accessed via `import ssl` statement).
NOTE: This has been tested with Python 3.11+ and Requests v2.30+
"""


# region Imports
# Script Dependencies:
#   - requests
#   - csv
#   - json
#   - typing

import requests as rq
# from typing import Generic, TypeVar
# endregion Imports

# region Author & Version
__author__: str = "Al Ferguson"
__updated__ = '2023-10-04 15:05:01'
__version__: str = "0.0.1"
# endregion Author & Version

# region Global Variables
API_URL: str = 'https://assets.stfc.space/data/latest/'
TRANSLATE_LANGUAGE = "en"
DETAIL_PATH = f'translations/{TRANSLATE_LANGUAGE}/'

SYSTEMS: list = rq.get(f'{API_URL}system', timeout=5).json()
SYSTEMNAMES: list = rq.get(f'{API_URL}{DETAIL_PATH}systems', timeout=5).json()
# endregion Global Variables

# region Functions


def jsonvalue(name: list, key: int):
    """jsonvalue returns Text versions of Int Key values from a JSON
    Args:
        name (json): JSON to search for Text value
        key (int): Key to convert
    Returns:
        str: Text value for passed key
    """

    return [x['text'] for x in name if (int(x['id']) == key
                                        and x['key'] == 'name')][0]


def construct_systemnames(system: dict) -> str:
    """Construct system Name from system dictionary"""
    return f'"{jsonvalue(SYSTEMNAMES, system["id"])}"'


# endregion Functions

def main() -> None:
    """https://stfc.space Information retrieval & CSV build."""

    print('Writing System CSV:')
    with open("STFC Territories.csv", "w") as file:
        file.write(generate_system())


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
