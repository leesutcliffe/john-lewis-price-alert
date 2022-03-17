import azure.functions as func

from src.items import items
from src.start import start


def main(timer: func.TimerRequest) -> None:
    start(items)
