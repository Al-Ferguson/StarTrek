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
# __all__ = ""
__author__: str = "Al Ferguson"
__version__: str = "0.0.7"
# endregion Author & Version

# region Global Variables
API_URL: str = "https://api.stfc.dev/v1/"
DETAIL_PATH = "translations/en/"
# endregion Author & Version

# region Functions


def getjsonvalue(name: list, key: int):
    """getjsonvalue returns Text versions of Int Key values from a JSON
    Args:
        name (json): JSON to search for Text value
        key (int): Key to convert
    Returns:
        str: Text value for passed key
    """

    return [x['text'] for x in name if (int(x['id']) == key and x['key'] == 'name')][0]


def shipimport(factions: list) -> str:
    """shipimport Builds the SQL for the STFC Ships Import File
    Args:
        factions (json): STFC Factions JSON
    Returns:
        str: IMPORT SQL for STFC Ships
    """
    ships = rq.get(API_URL + 'ship').json()
    names = rq.get(API_URL + DETAIL_PATH + 'ships').json()
    types = rq.get(API_URL + DETAIL_PATH + 'ship_type').json()
    result: str = ''
    
    for ship in ships:
        if not result:
            result = 'INSERT INTO `StfcShips` (`ShipID`, `ShipName`, `ShipLevel`, `ShipType`,`ShipFaction`) VALUES\n'
        else:
            result += ",\n"

        ship_name = getjsonvalue(names, ship['id'])
        ship_type = getjsonvalue(types, ship['hull_type']).capitalize()
        faction = getjsonvalue(factions, ship['faction'])
        result += f'({ship["id"]}, "{ship_name}", {ship["grade"]}, "{ship_type}", "{faction}")'

    return result


def systemimport(factions: list) -> str:
    """systemimport Builds the SQL for the STFC Systems Import File
    Args:
        factions (json): STFC Factions JSON
    Returns:
        str: IMPORT SQL for STFC Systems
    """
    systems = rq.get(API_URL + 'system').json()
    names = rq.get(API_URL + DETAIL_PATH + 'systems').json()
    result: str = ''
    
    for system in systems:
        if not result:
            result = 'INSERT INTO `StfcSystems` (`SystemID`, `SystemName`, `SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`) VALUES\n'
        else:
            result += ",\n"

        system_name = getjsonvalue(names, system['id'])
        faction = getjsonvalue(factions, system['faction'])
        result += f'({system["id"]}, "{system_name}", {system["level"]}, {system["est_warp"]}, "{faction}", {system["is_deep_space"]})'

    return result

# endregion Functions


def main() -> None:
    """Driver for https://stfc.space Information retrieval."""
    # region Initialize Interfaces

    factions = rq.get(API_URL + DETAIL_PATH + 'factions').json()  
    import_end = ";\n\nCOMMIT;\n\n"

    # endregion

    print('Writing Ships IMPORT SQL:')
    with open("STFC Pirate 2 Ships.sql", "w") as file:
        file.write(shipimport(factions) + import_end)

    print('Writing Systems IMPORT SQL:')
    with open("STFC Pirate 3 Systems.sql", "w") as file:
        file.write(systemimport(factions) + import_end)


if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
