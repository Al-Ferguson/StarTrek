"""stfc_get.py - Pull data from https://stfc.space and write to CSV file.

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
__updated__ = "2025-01-29 17:15:31"
__version__: str = "0.2.6"
# endregion Author & Version

# region Functions


def fetch_json(url: str, tout: int = 5) -> tuple:
    """Fetch JSON data from a given URL."""
    return tuple(rq.get(url, timeout=tout).json())


def generate_ship_import() -> str:
    """shipimport Builds the SQL for the STFC Ships Import File"""
    return SHIP_INSERT + ",\n".join(construct_ship_row(ship) for ship in SHIP)


def construct_ship_row(ship: dict) -> str:
    """Constructs a ship row string from the given dictionary."""
    factid: str = ship.get("faction", {}).get("loca_id", "0")
    return (
        f'({ship["id"]}, '
        f'{construct_shipnames(ship["loca_id"])}, '
        f'{ship["grade"]}, '
        f'"{SHIPTYPES[ship["hull_type"]]}", '
        f'{construct_faction(factid)})'
    )


def construct_shipnames(shipid: str) -> str:
    """Construct Ship Name from ships dictionary"""
    return f'"{get_json_value(SHIPS, shipid, "ship_name", "")}"'


def get_json_value(sdb: tuple, srchid: str, srkey: str, dflt: str = "") -> str:
    """Get a value from a JSON Dictionary"""
    return next((x["text"] for x in sdb
                 if (x["id"] == srchid and x["key"] == srkey)), dflt)


def construct_faction(factid: str) -> str:
    """Construct Faction Name from factions dictionary"""
    return f'"{get_json_value(FACTIONS, factid, "faction_name", "Neutral")}"'


def generate_system_import() -> str:
    """systemimport Builds the SQL for the STFC Systems Import File"""
    return SYSTEM_INSERT + ",\n".join(construct_system_row(system)
                                      for system in SYSTEM)


def construct_system_row(system: dict) -> str:
    """Builds SQL import data line from system dictionary."""
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
        f'{system["is_deep_space"]}, '
        f'{system["is_mirror_universe"]})'
    )


def construct_systemnames(systid: str) -> str:
    """Construct System Name from systems dictionary"""
    return f'"{get_json_value(SYSTEMS, f"{systid}", "title")}"'


# endregion Functions

# region Global Variables
API_URL: str = "https://assets.stfc.space/data/latest"
TRANSLATE_LANGUAGE = "en"
DETAIL_URL: str = f"{API_URL}/translations/{TRANSLATE_LANGUAGE}"

SHIP_INSERT: str = (
    "INSERT INTO `StfcShips` (`ShipID`, `ShipName`,"
    "`ShipLevel`, `ShipType`,`ShipFaction`) VALUES\n"
)
SYSTEM_INSERT: str = (
    "INSERT INTO `StfcSystems` (`SystemID`, `SystemName`, "
    "`SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`, "
    "`MirrorSpace`) VALUES\n"
)
SQL_END = ";\n\nCOMMIT;\n\n"

VERSION: str = rq.get(f"{API_URL}/version.txt", timeout=5).text

SHIP: tuple = fetch_json(f"{API_URL}/ship/summary.json?version={VERSION}")
SHIPS: tuple = fetch_json(f"{DETAIL_URL}/ships.json?version={VERSION}")
SYSTEM: tuple = fetch_json(f"{API_URL}/system/summary.json?version={VERSION}")
SYSTEMS: tuple = fetch_json(f"{DETAIL_URL}/systems.json?version={VERSION}")
FACTIONS: tuple = fetch_json(f"{DETAIL_URL}/factions.json?version={VERSION}")

SHIPTYPES: tuple = ("Interceptor", "Survey", "Explorer", "Battleship")
# endregion Global Variables


def main() -> None:
    """https://stfc.space Information retrieval & Import SQL build."""

    print("Writing Ships IMPORT SQL:")
    ships_sql = generate_ship_import() + SQL_END
    with open("STFC Pirate 2 Ships.sql", "w", encoding="utf-8") as file:
        file.write(ships_sql)

    print("Writing Systems IMPORT SQL:")
    systems_sql = generate_system_import() + SQL_END
    with open("STFC Pirate 3 Systems.sql", "w", encoding="utf-8") as file:
        file.write(systems_sql)


if __name__ == "__main__":
    print(f"\n{__doc__}\n")
    main()
