"""StfcGet.py - Pull data from https://stfc.space and write to CSV file.

NOTE: To access a REST API via https, the Python implementation must be
      compiled with SSL support (accessed via `import ssl` statement).
NOTE: This application requires the Requests Module from PyPi. This can
      be installed by running `pip install -U requests`.
NOTE: This has been tested with  Python 3.9+ and Requests v2.30.0.
"""


# region Imports

import requests as rq
import json

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

def getjsonvalue(json_name: json, key: int) -> str:
    return [x['text'] for x in json_name if (int(x['id']) == key and
                                            x['key'] == 'name')][0]

# endregion Functions


def main() -> None:
    """Driver for https://stfc.space Information retrieval."""
    # region Initialize Interfaces

    ships = rq.get(API_URL + 'ship').json()
    ship_names = rq.get(API_URL + DETAIL_PATH + 'ships').json()
    ship_types = rq.get(API_URL + DETAIL_PATH + 'ship_type').json()
    factions = rq.get(API_URL + DETAIL_PATH + 'factions').json()

    systems = rq.get(API_URL + 'system').json()
    system_names = rq.get(API_URL + DETAIL_PATH + 'systems').json()

    # endregion

    print('Writing Ships IMPORT SQL:')
    with open("STFC Pirate Ships.sql", "w") as file:
        output = ''
        for ship in ships:
            if not output:
                file.write('INSERT INTO `StfcShips` (`ShipID`, `ShipName`, `ShipLevel`, `ShipType`,`ShipFaction`) VALUES\n')
            else:
                file.write(output + ",\n")

            ship_name = getjsonvalue(ship_names, ship['id'])
            ship_type = getjsonvalue(ship_types, ship['hull_type']).capitalize()
            faction = getjsonvalue(factions, ship['faction'])
            output = f'({ship["id"]}, "{ship_name}", {ship["grade"]}, "{ship_type}", "{faction}")'

        file.write(output + ";\n\nCOMMIT;\n\n")

    print('Writing Systems IMPORT SQL:')
    with open("STFC Pirate Systems.sql", "w") as file:
        output = ''
        for system in systems:
            if not output:
                file.write('INSERT INTO `StfcSystems` (`SystemID`, `SystemName`, `SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`) VALUES\n')
            else:
                file.write(output + ",\n")

            system_name = getjsonvalue(system_names, system['id'])
            faction = getjsonvalue(factions, system['faction'])
            output = f'({system["id"]}, "{system_name}", {system["level"]}, {system["est_warp"]}, "{faction}", {system["is_deep_space"]})'

        file.write(output + ";\n\nCOMMIT;\n\n")

if __name__ == "__main__":
    print(f"\n{__doc__}\n")

    main()
