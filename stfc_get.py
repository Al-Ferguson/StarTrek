# Copyright (c) 2026 Al Ferguson
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

import json
from pathlib import Path

import httpx2

# endregion Imports

# region Author & Version
__author__: str = "Al Ferguson"
__updated__ = "2026-11-18 14:17:22"
__version__: str = "0.3.0"
# endregion Author & Version

# region Functions


def generate_ship_import() -> str:
    """Build the SQL for the STFC Ships Import File."""
    ship_rows = [construct_ship_row(ship) for ship in SHIP]
    return SHIP_INSERT + ",\n".join(ship_rows)


def construct_ship_row(ship: dict) -> str:
    """Construct a ship row string from the given dictionary."""
    ship_id = str(ship["id"])
    ship_name = str(SHIPS[ship["loca_id"]].get("ship_name", ""),
)
    grade = str(ship["grade"])
    ship_type = SHIPTYPES[ship["hull_type"]]
    faction = str(
        FACTIONS.get(ship["faction"].get("loca_id")).get("faction_name", "Neutral"),
    )

    return f'({ship_id}, {ship_name}, {grade}, "{ship_type}", {faction})'


def generate_system_import() -> str:
    """Build SQL for the STFC Systems Import File."""
    return SYSTEM_INSERT + ",\n".join(
        construct_system_row(system) for system in SYSTEM
    )


def construct_system_row(system: dict) -> str:
    """Build SQL import data line from system dictionary."""
    try:
        factid: str = system["hostiles"][0]["faction"]["loca_id"]
    except (KeyError, IndexError, TypeError):
        factid = "0"

    row_data = [
        str(system["id"]),
        str(SYSTEMS[system["loca_id"]]["title"]),
        str(system["level"]),
        str(system["est_warp"]),
        str(FACTIONS[factid]["faction_name"]),
        str(system["is_deep_space"]),
        str(system["is_mirror_universe"]),
    ]

    return f"({', '.join(row_data)})"


# endregion Functions

# region Global Variables
SHIP_INSERT: str = (
    "INSERT INTO `StfcShips` (`ShipID`, `ShipName`,`ShipLevel`, "
    "`ShipType`,`ShipFaction`) VALUES\n"
)
SYSTEM_INSERT: str = (
    "INSERT INTO `StfcSystems` (`SystemID`, `SystemName`, "
    "`SystemLevel`, `SystemWarpDist`, `SystemType`, `DarkSpace`, "
    "`MirrorSpace`) VALUES\n"
)
SQL_END = ";\n\nCOMMIT;\n\n"

API_URL: str = "https://data.stfc.space"
TRANSLATE_LANGUAGE = "en"
DETAIL: str = f"translations/{TRANSLATE_LANGUAGE}"

with httpx2.Client(
    base_url="https://data.stfc.space",
    headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US, en;q=0.9",
    },
    http2=True,
) as client:
    VERSION: str = client.get("/version.txt").text
    SHIP = json.loads(client.get(f"ship/summary.json?version={VERSION}").text)
    SHIPS = json.loads(
        client.get(f"/{DETAIL}/ships.json?version={VERSION}").text,
    )
    SYSTEM = json.loads(
        client.get(f"/planetary_base/summary.json?version={VERSION}").text,
    )
    SYSTEMS = json.loads(
        client.get(f"/{DETAIL}/systems.json?version={VERSION}").text,
    )
    FACTIONS = json.loads(
        client.get(f"/{DETAIL}/factions.json?version={VERSION}").text,
    )

SHIPTYPES: tuple = ("Interceptor", "Survey", "Explorer", "Battleship")

# endregion Global Variables


def main() -> None:
    """https://data.stfc.space Information retrieval & Import SQL build."""
    print("Writing Ships IMPORT SQL:")  # noqa: T201
    ships_sql = generate_ship_import() + SQL_END
    with Path("STFC Pirate 2 Ships.sql").open("w", encoding="utf-8") as file:
        file.write(ships_sql)

    print("Writing Systems IMPORT SQL:")  # noqa: T201
    systems_sql = generate_system_import() + SQL_END
    with Path("STFC Pirate 3 Systems.sql").open("w", encoding="utf-8") as file:
        file.write(systems_sql)


if __name__ == "__main__":
    print(f"\n{__doc__}\n")  # noqa: T201
    main()
