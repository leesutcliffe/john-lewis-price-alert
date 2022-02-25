import logging

import azure.functions as func

from src.start import start


def main(timer: func.TimerRequest) -> None:
    current_price = start()
    logging.info(f"current price is {current_price}")

