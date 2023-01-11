"""StfcGet.py - Pull data from https://stfc.space and write to CSV file.

NOTE: To access a REST API via https, the Python implementation must be
      compiled with SSL support (accessed via `import ssl` statement).
NOTE: This application requires the Requests Module from PyPi. This can
      be installed by running `pip install -U requests`.
NOTE: This has been tested with Python 3.9+ and Requests v2.30+
"""


# region Imports
import requests as rq
# endregion Imports

# region Author & Version
__author__: str = "Al Ferguson"
__updated__ = '2023-01-11 12:07:14'
__version__: str = "0.1.2"
# endregion Author & Version

# region Global Variables
API_URL: str = 'https://api.stfc.dev/v1/'
TRANSLATE_LANGUAGE = "en"
DETAIL_PATH = f'translations/{TRANSLATE_LANGUAGE}/'

SHIP_INSERT: str = 'INSERT INTO `StfcShips` (`ShipID`, `ShipName`,' \
    '`ShipLevel`, `ShipType`,`ShipFaction`) VALUES\n'
SYSTEM_INSERT: str = 'INSERT INTO `StfcSystems` (`SystemID`, `SystemName`,' \
    '`SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`) VALUES\n'
SQL_END = ";\n\nCOMMIT;\n\n"

SHIPS: list = rq.get(f'{API_URL}ship').json()
SHIPNAMES: list = rq.get(f'{API_URL}{DETAIL_PATH}ships').json()
SHIPTYPES: list = rq.get(f'{API_URL}{DETAIL_PATH}ship_type').json()
SYSTEMS: list = rq.get(f'{API_URL}system').json()
SYSTEMNAMES: list = rq.get(f'{API_URL}{DETAIL_PATH}systems').json()
FACTIONS = rq.get(f'{API_URL}{DETAIL_PATH}factions').json()
# endregion Author & Version

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

    result: str = ''
    for ship in SHIPS:
        if not result:
            result = SHIP_INSERT + construct_ship_row(ship)
        else:
            result += ",\n" + construct_ship_row(ship)

    return result


def construct_ship_row(ship: dict) -> str:
    """data builds IMPORT Data Line"""
    return f'({ship["id"]}, {construct_name(ship)}, \
{construct_grade(ship)}, {construct_hull_type(ship)}, \
{construct_faction(ship)})'


def construct_name(ship: dict) -> str:
    """Construct ship Name from ship dictionary"""
    return f'"{jsonvalue(SHIPNAMES, ship["id"])}"'


def construct_grade(ship: dict) -> str:
    """Construct ship grade from ship dictionary"""
    return f'{ship["grade"]}'


def construct_hull_type(ship: dict) -> str:
    """Construct hull from ship dictionary"""
    return f'"{jsonvalue(SHIPTYPES, ship["hull_type"]).capitalize()}"'


def construct_faction(ship: dict) -> str:
    """Construct faction from ship dictionary"""
    return f'"{jsonvalue(FACTIONS, ship["faction"])}"'


def generate_system_import() -> str:
    """systemimport Builds the SQL for the STFC Systems Import File
    Args:
        None
    Returns:
        str: IMPORT SQL for STFC Systems
    """

    result: str = ''
    for system in SYSTEMS:
        if not result:
            result = SYSTEM_INSERT + construct_system_row(system)
        else:
            result += ",\n" + construct_system_row(system)

    return result


def construct_system_row(system: dict) -> str:
    """data builds IMPORT Data Line"""
    return f'({system["id"]}, "{jsonvalue(SYSTEMNAMES, system["id"])}",' \
        f'{system["level"]}, {system["est_warp"]},' \
        f'"{jsonvalue(FACTIONS, system["faction"])}",' \
        f'{system["is_deep_space"]})'

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
