from azure.storage.blob import BlobServiceClient


class DataStore:
    blob_service_client: BlobServiceClient

    def __init__(self, blob_service_client: BlobServiceClient):
        self.blob_service_client = blob_service_client

    def save_data(self, data: str) -> None:
        blob_client = self.blob_service_client.get_blob_client("data", "ercol_prices.csv")
        blob_client.upload_blob(data)
