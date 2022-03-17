import os
from typing import List

from azure.storage.blob import BlobServiceClient

from src.alert import alert
from src.constants import BLOB_NAME, CONTAINER_NAME, STORAGE_CONNECTION
from src.models.models import Item
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore


def start(items: List[Item]) -> None:
    container_name = os.getenv(CONTAINER_NAME)
    storage_connection = str(os.getenv(STORAGE_CONNECTION))
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection)
    datastore = DataStore(blob_service_client, container_name, BLOB_NAME)
    price_checker = PriceChecker(datastore)

    for item in items:
        current_price = price_checker.get_current_price(item)
        previous_price = price_checker.previous_price()
        if current_price < previous_price:
            alert.send(item, previous_price, current_price)
        price_checker.save_price(current_price)
