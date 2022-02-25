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
    pc = PriceChecker(datastore)
    price = pc.get_price(ERCOL_URL, requests.get, save_price=True)
    return price


if __name__ == "__main__":
    start()
