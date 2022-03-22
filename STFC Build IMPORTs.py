"""StfcGet.py - Pull data from https://stfc.space and write to CSV file.

NOTE: To access a REST API via https, the Python implementation must be
      compiled with SSL support (accessed via `import ssl` statement).
NOTE: This application requires the Requests Module from PyPi. This can
      be installed by running `pip install -U requests`.
NOTE: This has been tested with  Python 3.9+ and Requests v2.30.0.
"""


# region Imports
import requests as rq
# endregion Imports

# region Author & Version
__author__: str = "Al Ferguson"
__updated__ = '2022-03-21 20:24:43'
__version__: str = "0.1.2"
# endregion Author & Version

# region Global Variables
API_URL: str = 'https://api.stfc.dev/v1/'
TRANSLATE_LANGUAGE = "en"
DETAIL_PATH = f'translations/{TRANSLATE_LANGUAGE}/'

SHIPS: list = rq.get(f'{API_URL}ship').json()
SHIPNAMES: list = rq.get(f'{API_URL}{DETAIL_PATH}ships').json()
SHIPTYPES: list = rq.get(f'{API_URL}{DETAIL_PATH}ship_type').json()
SYSTEMS: list = rq.get(f'{API_URL}system').json()
SYSTEMNAMES: list = rq.get(f'{API_URL}{DETAIL_PATH}systems').json()
FACTIONS = rq.get(f'{API_URL}{DETAIL_PATH}factions').json()
# endregion Author & Version

# region Functions


def jsonvalue(name: list, key: int):
    """getjsonvalue returns Text versions of Int Key values from a JSON
    Args:
        name (json): JSON to search for Text value
        key (int): Key to convert
    Returns:
        str: Text value for passed key
    """

    return [x['text'] for x in name if (int(x['id']) == key
                                        and x['key'] == 'name')][0]


def shipimport() -> str:
    """shipimport Builds the SQL for the STFC Ships Import File
    Args:
        None
    Returns:
        str: IMPORT SQL for STFC Ships
    """

    # region Function Variables
    result: str = ''
    # endregion Function Variables

    for ship in SHIPS:
        if not result:
            result = 'INSERT INTO `StfcShips` (`ShipID`, `ShipName`,' \
                '`ShipLevel`, `ShipType`,`ShipFaction`) VALUES\n'
        else:
            result += ",\n"
        result += shipdata(ship)

    return result


def shipdata(ship: dict) -> str:
    """data builds IMPORT Data Line"""
    return f'({ship["id"]},' \
        f'"{jsonvalue(SHIPNAMES, ship["id"])}",' \
        f'{ship["grade"]},' \
        f'"{jsonvalue(SHIPTYPES, ship["hull_type"]).capitalize()}",' \
        f'"{jsonvalue(FACTIONS, ship["faction"])}")'


def systemimport() -> str:
    """systemimport Builds the SQL for the STFC Systems Import File
    Args:
        None
    Returns:
        str: IMPORT SQL for STFC Systems
    """
    # region Function Variables
    result: str = ''
    # endregion Function Variables

    for system in SYSTEMS:
        if not result:
            result = 'INSERT INTO `StfcSystems` (`SystemID`, `SystemName`,' \
                '`SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`)' \
                'VALUES\n'
        else:
            result += ",\n"
        result += systemdata(system)

    return result


def systemdata(system: dict) -> str:
    """data builds IMPORT Data Line"""
    return f'({system["id"]}, "{jsonvalue(SYSTEMNAMES, system["id"])}",' \
        f'{system["level"]}, {system["est_warp"]},' \
        f'"{jsonvalue(FACTIONS, system["faction"])}",' \
        f'{system["is_deep_space"]})'

# endregion Functions


def main() -> None:
    """Driver for https://stfc.space Information retrieval."""
    # region Initialize Variables

    import_end = ";\n\nCOMMIT;\n\n"

    # endregion

    print('Writing Ships IMPORT SQL:')
    with open("STFC Pirate 2 Ships.sql", "w") as file:
        file.write(shipimport() + import_end)

    print('Writing Systems IMPORT SQL:')
    with open("STFC Pirate 3 Systems.sql", "w") as file:
        file.write(systemimport() + import_end)


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
