import os

from azure.storage.blob import BlobServiceClient

from src.alert import alert
from src.constants import ERCOL_URL
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore


def start() -> float:
    container_name = os.getenv("CONTAINER_NAME")
    storage_connection = str(os.getenv("STORAGE_CONNECTION"))
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection)
    datastore = DataStore(blob_service_client, container_name, "prices.csv")
    ercol = PriceChecker(datastore)

    current_price = ercol.get_current_price(ERCOL_URL)
    previous_price = ercol.previous_price()
    if current_price < previous_price:
        alert.send(previous_price, current_price)
    ercol.get_current_price(ERCOL_URL, save_price=True)
    return current_price


if __name__ == "__main__":
    start()
