import os

from azure.storage.blob import BlobServiceClient

from src.alert import alert
from src.items import items
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore


def start() -> float:
    container_name = os.getenv("CONTAINER_NAME")
    storage_connection = str(os.getenv("STORAGE_CONNECTION"))
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection)
    datastore = DataStore(blob_service_client, container_name, "prices.csv")
    price_checker = PriceChecker(datastore)

    for item in items:
        current_price = price_checker.get_current_price(item)
        previous_price = price_checker.previous_price()
        if current_price < previous_price:
            alert.send(previous_price, current_price)
        price_checker.save_price(current_price)
    return current_price


if __name__ == "__main__":
    start()
