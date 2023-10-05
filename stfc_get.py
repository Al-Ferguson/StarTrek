"""stfc_get.py - Pull data from https://stfc.space and write to CSV file.

NOTE: This application requires the Requests Module from PyPi. This can
      be installed by running `pip install -U requests`.
NOTE: To access a REST API via https, the Python implementation must be
      compiled with SSL support (accessed via `import ssl` statement).
NOTE: This has been tested with Python 3.9+ and Requests v2.30+
"""


# region Imports
import requests as rq
# endregion Imports

# region Author & Version
__author__: str = "Al Ferguson"
__updated__ = '2023-10-04 23:41:58'
__version__: str = "0.1.2"
# endregion Author & Version

# region Global Variables
API_URL: str = 'https://assets.stfc.space/data/latest'
TRANSLATE_LANGUAGE = "en"
DETAIL_URL: str = f'{API_URL}/translations/{TRANSLATE_LANGUAGE}'

SHIP_INSERT: str = 'INSERT INTO `StfcShips` (`ShipID`, `ShipName`,' \
    '`ShipLevel`, `ShipType`,`ShipFaction`) VALUES\n'
SYSTEM_INSERT: str = 'INSERT INTO `StfcSystems` (`SystemID`, `SystemName`,' \
    '`SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`) VALUES\n'
SQL_END = ";\n\nCOMMIT;\n\n"

SHIP: list = rq.get(f'{API_URL}/ship/summary.json', timeout=5).json()
SHIPS: list = rq.get(f'{DETAIL_URL}/ships.json', timeout=5).json()
SHIPTYPES: list = rq.get(f'{DETAIL_URL}/ship_type.json', timeout=5).json()
SYSTEM: list = rq.get(f'{API_URL}/system/summary.json', timeout=5).json()
SYSTEMS: list = rq.get(f'{DETAIL_URL}/systems.json', timeout=5).json()
FACTIONS = rq.get(f'{DETAIL_URL}/factions.json', timeout=5).json()
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


def generate_ship_import() -> str:
    """shipimport Builds the SQL for the STFC Ships Import File
    Args:
        None
    Returns:
        str: IMPORT SQL for STFC Ships
    """
    result = [construct_ship_row(ship) for ship in SHIP]

    return SHIP_INSERT + ",\n".join(result)


def construct_ship_row(ship: dict) -> str:
    """data builds IMPORT Data Line"""
    return f'({ship["id"]}, {construct_shipnames(ship)},\
 {ship["grade"]}, {construct_hull_type(ship)},\
 {construct_faction(ship)})'


def construct_shipnames(ship: dict) -> str:
    """Construct ship Name from ship dictionary"""
    return f'"{jsonvalue(SHIPS, ship["id"])}"'


def construct_hull_type(ship: dict) -> str:
    """Construct hull from ship dictionary"""
    return f'"{jsonvalue(SHIPTYPES, ship["hull_type"]).capitalize()}"'


def construct_faction(dictionary: dict) -> str:
    """Construct faction from a dictionary"""
    return f'"{jsonvalue(FACTIONS, dictionary["faction"])}"'


def generate_system_import() -> str:
    """systemimport Builds the SQL for the STFC Systems Import File
    Args:
        None
    Returns:
        str: IMPORT SQL for STFC Systems
    """
    result = [construct_system_row(system) for system in SYSTEM]

    return SYSTEM_INSERT + ",\n".join(result)


def construct_system_row(system: dict) -> str:
    """data builds IMPORT Data Line"""
    return f'({system["id"]}, {construct_systemnames(system)},\
 {system["level"]}, {system["est_warp"]}, {construct_faction(system)},\
 {system["is_deep_space"]})'


def construct_systemnames(system: dict) -> str:
    """Construct system Name from system dictionary"""
    return f'"{jsonvalue(SYSTEMS, system["id"])}"'


# endregion Functions


def main() -> None:
    """https://stfc.space Information retrieval & Import SQL build."""

    print('Writing Ships IMPORT SQL:')
    with open("STFC Pirate 2 Ships.sql", "w") as file:
        file.write(generate_ship_import() + SQL_END)

    print('Writing Systems IMPORT SQL:')
    with open("STFC Pirate 3 Systems.sql", "w") as file:
        file.write(generate_system_import() + SQL_END)


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
