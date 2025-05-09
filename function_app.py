import logging
import azure.functions as func
import asyncio
from common.api_calls import *

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 0 1 * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False
)
def titan6hours() -> None:
    get_titan_stats()
