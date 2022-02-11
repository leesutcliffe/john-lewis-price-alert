import requests
from azure.storage.blob import BlobServiceClient

from price_alert_app.src.constants import ERCOL_URL
from price_alert_app.src.price_checker.price_checker import PriceChecker
from price_alert_app.src.repository.datastore import DataStore
from price_alert_app.tests.conftest import AZURITE_STORAGE_CONNECTION


def main() -> float:
    blob_service_client = BlobServiceClient.from_connection_string(AZURITE_STORAGE_CONNECTION)
    datastore = DataStore(blob_service_client, "prices.csv")
    pc = PriceChecker(datastore)
    price = pc.get_price(ERCOL_URL, requests.get, save_price=True)
    print(f"Price: {price}")
    return price


if __name__ == "__main__":
    main()
