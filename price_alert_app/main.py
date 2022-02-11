import datetime
import logging

import azure.functions as func

from price_alert_app.src.start import start


def main(timer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    if timer.past_due:
        current_price = start()
        logging.info(f"current price is {current_price}")

    logging.info("Python timer trigger function ran at %s", utc_timestamp)
