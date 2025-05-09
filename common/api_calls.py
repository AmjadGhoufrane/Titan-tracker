import requests
import asyncio
import json
from common.db_calls import *


def get_titan_stats():
    url = f"https://zkillboard.com/api/stats/groupID/30/"

    headers = {
        "User-Agent": "TitanTracker/1.0 (Contact: admin@example.com)",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    ingest_all_stats(data)
