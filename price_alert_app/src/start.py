import os

import requests
from azure.storage.blob import BlobServiceClient

from src.constants import ERCOL_URL
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore


def start() -> float:
    container_name = os.getenv("CONTAINER_NAME")
    storage_connection = str(os.getenv("STORAGE_CONNECTION"))
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection)
    datastore = DataStore(blob_service_client, container_name, "prices.csv")
    ercol = PriceChecker(datastore)

    current_price = ercol.get_current_price(ERCOL_URL, requests.get)
    previous_price = ercol.previous_price()
    # TODO: previous price may not exist
    if current_price < previous_price:
        ercol.send_email()
    ercol.get_current_price(ERCOL_URL, requests.get, save_price=True)
    return current_price


if __name__ == "__main__":
    start()
