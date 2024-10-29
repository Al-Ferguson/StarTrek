"""stfc_territories.py - Pull https://stfc.space data and write CSV file.

NOTE: This application requires the Requests Module from PyPi. This can
      be installed by running `pip install -U requests`.
NOTE: To access a REST API via https, the Python implementation must be
      compiled with SSL support (accessed via `import ssl` statement).
NOTE: This has been tested with Python 3.9+ and Requests v2.32+
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
__updated__ = "2024-10-28 23:07:08"
__version__: str = "0.0.5"
# endregion Author & Version

# region Functions


def fetch_json(url: str, tout: int = 5) -> tuple:
    """Fetch JSON data from a given URL."""
    return tuple(rq.get(url, timeout=tout).json())


def get_json_value(sdb: list, srchid: str, skey: str, dflt: str) -> str:
    """Get a value from a JSON Dictionary"""
    return next((x["text"] for x in sdb if
                 (x["id"] == srchid and x["key"] == skey)), dflt)


def jsonvalue(name: list, key: int):
    """jsonvalue returns Text versions of Int Key values from a JSON"""
    lookup = {int(item["id"]): item["text"] for
              item in name if item["key"] == "name"}
    return lookup.get(key, "")


def construct_faction(factid: str) -> str:
    """Construct Faction Name from factions dictionary"""
    return f'"{get_json_value(FACTIONS, factid, "faction_name", "Neutral")}"'


def generate_system() -> str:
    """systemimport Builds the SQL for the STFC Systems Import File"""
    return ",\n".join([construct_system_row(system) for system in SYSTEM])


def construct_system_row(system: dict) -> str:
    """data builds IMPORT Data Line"""
    try:
        factid: str = system["hostiles"][0]["faction"]["loca_id"]
    except IndexError:
        factid = "0"
    return (
        f'({system["id"]}, '
        f'{construct_systemnames(system["id"])}, '
        f'{system["level"]}, '
        f'{system["est_warp"]}, '
        f"{construct_faction(factid)}, "
        f'{system["is_deep_space"]})'
    )


def construct_systemnames(systid: str) -> str:
    """Construct System Name from systems dictionary"""
    return f'"{get_json_value(SYSTEMS, f"{systid}", "title", "")}"'


# endregion Functions

# region Global Variables
API_URL: str = "https://assets.stfc.space/data/latest/"
TRANSLATE_LANGUAGE = "en"
DETAIL_URL: str = f"{API_URL}/translations/{TRANSLATE_LANGUAGE}"

VERSION: str = rq.get(f"{API_URL}/version.txt", timeout=5).text

SYSTEM: tuple = fetch_json(f"{API_URL}/system/summary.json?version={VERSION}")
SYSTEMS: tuple = fetch_json(f"{DETAIL_URL}/systems.json?version={VERSION}")
FACTIONS: tuple = fetch_json(f"{DETAIL_URL}/factions.json?version={VERSION}")
# endregion Global Variables


def main() -> None:
    """https://stfc.space Information retrieval & CSV build."""

    print("Writing System CSV:")
    with open("STFC Territories.csv", "w", encoding="utf-8") as file:
        file.write(generate_system())


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
