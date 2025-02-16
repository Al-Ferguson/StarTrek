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
__updated__ = "2025-02-15 19:41:31"
__version__: str = "0.0.5"
# endregion Author & Version

# region Functions


def get_json_value(
    json_data: tuple[dict], srchid: str, srchkey: str, dflt: str = ""
) -> str:
    """Get a value from a JSON Dictionary for the given key"""
    return next(
        (item["text"]
         for item in json_data
         if (
             item["id"] == srchid and
             item["key"] == srchkey
             )),
        dflt
        )


def construct_faction(factid: str) -> str:
    """Construct Faction Name from factions dictionary"""
    return f'"{get_json_value(FACTIONS, factid, "faction_name", "Neutral")}"'


def generate_system() -> str:
    """generate_system Builds the SQL for the STFC Systems Import File"""
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

SYSTEM: tuple[dict] = rq.get(
    f"{API_URL}/system/summary.json?version={VERSION}",
    timeout=5
).json()
SYSTEMS: tuple[dict] = rq.get(f"{DETAIL_URL}/systems.json?version={VERSION}",
                              timeout=5).json()
FACTIONS: tuple[dict] = rq.get(f"{DETAIL_URL}/factions.json?version={VERSION}",
                               timeout=5).json()

# endregion Global Variables


def main() -> None:
    """https://stfc.space Information retrieval & CSV build."""

    print("Writing System CSV:")
    with open("STFC Territories.csv", "w", encoding="utf-8") as file:
        file.write(generate_system())


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
