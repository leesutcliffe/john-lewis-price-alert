import os

import requests
from azure.storage.blob import BlobServiceClient

from price_alert_app.src.constants import ERCOL_URL
from price_alert_app.src.price_checker.price_checker import PriceChecker
from price_alert_app.src.repository.datastore import DataStore


def start() -> float:
    storage_connection = str(os.getenv("STORAGE_CONNECTION"))
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection)
    datastore = DataStore(blob_service_client, "prices.csv")
    pc = PriceChecker(datastore)
    price = pc.get_price(ERCOL_URL, requests.get, save_price=True)
    return price


if __name__ == "__main__":
    start()
