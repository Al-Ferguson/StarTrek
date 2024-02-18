"""stfc_territories.py - Pull https://stfc.space data and write CSV file.

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

# endregion Imports

# region Author & Version
__author__: str = "Al Ferguson"
__updated__ = "2024-02-18 05:35:15"
__version__: str = "0.0.2"
# endregion Author & Version

# region Global Variables
API_URL: str = "https://assets.stfc.space/data/latest/"
TRANSLATE_LANGUAGE = "en"
DETAIL_URL: str = f"{API_URL}/translations/{TRANSLATE_LANGUAGE}"

SYSTEM: list = rq.get(f"{API_URL}system/summary.json", timeout=5).json()
SYSTEM_DETAILS: list = rq.get(f"{DETAIL_URL}/systems.json", timeout=5).json()
FACTIONS = rq.get(f"{DETAIL_URL}/factions.json", timeout=5).json()
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

    lookup = {int(item["id"]): item["text"] for item in name if item["key"] == "name"}
    return lookup.get(key, "")


def construct_faction(dictionary: dict) -> str:
    """Construct faction from a dictionary"""

    return f'"{jsonvalue(FACTIONS, dictionary["faction"])}"'


def generate_system() -> str:
    """systemimport Builds the SQL for the STFC Systems Import File
    Args:
        None
    Returns:
        str: IMPORT SQL for STFC Systems
    """

    result = [construct_system_row(system) for system in SYSTEM]
    return ",\n".join(result)


def construct_system_row(system: dict) -> str:
    """data builds IMPORT Data Line"""

    return f'({system["id"]}, {construct_systemnames(system)},\
 {system["level"]}, {system["est_warp"]}, {construct_faction(system)},\
 {system["is_deep_space"]})'


def construct_systemnames(system: dict) -> str:
    """Construct system Name from system dictionary"""

    return f'"{jsonvalue(SYSTEM_DETAILS, system["id"])}"'


# endregion Functions


def main() -> None:
    """https://stfc.space Information retrieval & CSV build."""

    print("Writing System CSV:")
    with open("STFC Territories.csv", "w", encoding="utf-8") as file:
        file.write(generate_system())


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
