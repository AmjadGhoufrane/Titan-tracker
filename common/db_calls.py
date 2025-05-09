import pymysql
import io
from common.orm import DB
import datetime


@DB
def ingest_months(months: dict, current_date=None, conn=None) -> None:
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE `monthlyStats`")
    cursor.execute("commit")

    for k in months.keys():
        cursor.execute(
            f"INSERT INTO `monthlyStats` (`year`, `month`, `shipsDestroyed`, `iskDestroyed`) VALUES ({months[k]['year']}, {months[k]['month']}, {months[k]['shipsDestroyed']}, {months[k]['iskDestroyed']}) "
        )

    cursor.execute("commit")
    cursor.close()


@DB
def ingest_top_characters(top_lists: list, current_date=None, conn=None) -> None:
    cursor = conn.cursor()

    characters_list = None
    for top_list in top_lists:
        if top_list["type"] == "character":
            characters_list = top_list["values"]
            break

    if not characters_list:
        return

    if current_date is None:
        current_date = datetime.date.today().replace(day=1)

    year_month = current_date

    cursor.execute(f"DELETE FROM `topCharacters` WHERE `yearMonth` = '{year_month}'")

    for character in characters_list:
        cursor.execute(
            f"INSERT INTO `topCharacters` (`characterID`, `kills`, `name`, `yearMonth`) "
            f"VALUES ({character['characterID']}, {character['kills']}, '{character['characterName']}', '{year_month}')"
        )

    cursor.execute("commit")
    cursor.close()


@DB
def ingest_top_corporations(top_lists: list, current_date=None, conn=None) -> None:
    cursor = conn.cursor()

    corporations_list = None
    for top_list in top_lists:
        if top_list["type"] == "corporation":
            corporations_list = top_list["values"]
            break

    if not corporations_list:
        return

    if current_date is None:
        current_date = datetime.date.today().replace(day=1)

    year_month = current_date

    cursor.execute(f"DELETE FROM `topCorporations` WHERE `yearMonth` = '{year_month}'")

    for corporation in corporations_list:
        cursor.execute(
            f"INSERT INTO `topCorporations` (`corporationID`, `corporationName`, `corporationTicker`, `kills`, `yearMonth`) "
            f"VALUES ({corporation['corporationID']}, '{corporation['corporationName']}', '{corporation['cticker']}', {corporation['kills']}, '{year_month}')"
        )

    cursor.execute("commit")
    cursor.close()


@DB
def ingest_top_alliances(top_lists: list, current_date=None, conn=None) -> None:
    cursor = conn.cursor()

    alliances_list = None
    for top_list in top_lists:
        if top_list["type"] == "alliance":
            alliances_list = top_list["values"]
            break

    if not alliances_list:
        return

    if current_date is None:
        current_date = datetime.date.today().replace(day=1)

    year_month = current_date

    cursor.execute(f"DELETE FROM `topAlliances` WHERE `yearMonth` = '{year_month}'")

    for alliance in alliances_list:
        cursor.execute(
            f"INSERT INTO `topAlliances` (`allianceID`, `allianceName`, `allianceTicker`, `AllianceKills`, `yearMonth`) "
            f"VALUES ({alliance['allianceID']}, '{alliance['allianceName']}', '{alliance['aticker']}', {alliance['kills']}, '{year_month}')"
        )

    cursor.execute("commit")
    cursor.close()


@DB
def ingest_top_systems(top_lists: list, current_date=None, conn=None) -> None:
    cursor = conn.cursor()

    systems_list = None
    for top_list in top_lists:
        if top_list["type"] == "solarSystem":
            systems_list = top_list["values"]
            break

    if not systems_list:
        return

    if current_date is None:
        current_date = datetime.date.today().replace(day=1)

    year_month = current_date

    cursor.execute(f"DELETE FROM `topSystems` WHERE `yearMonth` = '{year_month}'")

    for system in systems_list:
        type_id = system["sunTypeID"] if system["sunTypeID"] is not None else 0
        cursor.execute(
            f"INSERT INTO `topSystems` (`systemID`, `systemName`, `typeID`, `kills`, `yearMonth`) "
            f"VALUES ({system['solarSystemID']}, '{system['solarSystemName']}', '{type_id}', {system['kills']}, '{year_month}')"
        )

    cursor.execute("commit")
    cursor.close()


@DB
def ingest_misc(data: dict, current_date=None, conn=None) -> None:
    cursor = conn.cursor()

    if not (
        "id" in data
        and "shipsLost" in data
        and "iskLost" in data
        and "shipsDestroyed" in data
        and "iskDestroyed" in data
    ):
        return

    if current_date is None:
        current_date = datetime.date.today().replace(day=1)

    year_month = current_date
    cursor.execute(
        f"DELETE FROM `miscData` WHERE `yearMonth` = '{year_month}' AND `idGroup` = {data['id']}"
    )

    cursor.execute(
        f"INSERT INTO `miscData` (`idGroup`, `shipsLost`, `iskLost`, `shipsDestroyed`, `iskDestroyed`, `yearMonth`) "
        f"VALUES ({data['id']}, {data['shipsLost']}, {data['iskLost']}, {data['shipsDestroyed']}, {data['iskDestroyed']}, '{year_month}')"
    )

    cursor.execute("commit")
    cursor.close()


def ingest_all_stats(data: dict) -> None:
    current_date = datetime.date.today().replace(day=1)

    ingest_months(data["months"])
    ingest_top_characters(data["topLists"])
    ingest_top_corporations(data["topLists"])
    ingest_top_alliances(data["topLists"])
    ingest_top_systems(data["topLists"])
    ingest_misc(data)
