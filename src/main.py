import requests
from azure.storage.blob import BlobServiceClient
from conftest import AZURITE_STORAGE_CONNECTION

from src.constants import ERCOL_URL
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore


def main() -> float:
    blob_service_client = BlobServiceClient.from_connection_string(AZURITE_STORAGE_CONNECTION)
    datastore = DataStore(blob_service_client, "prices.csv")
    pc = PriceChecker(datastore)
    price = pc.get_price(ERCOL_URL, requests.get, save_price=True)
    print(f"Price: {price}")
    return price


"""
get price
if csv exists, add to current
else save to new
"""

if __name__ == "__main__":
    main()
