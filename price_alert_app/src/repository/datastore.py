from azure.storage.blob import BlobClient, BlobServiceClient


class DataStore:
    blob_service_client: BlobServiceClient
    blob_name: str
    blob_client: BlobClient

    def __init__(self, blob_service_client: BlobServiceClient, container_name: str, blob_name: str):
        self.blob_service_client = blob_service_client
        self.container_name = container_name
        self.blob_name = blob_name
        self.blob_client = self.blob_service_client.get_blob_client(self.container_name, self.blob_name)

    def save_data(self, data: str) -> None:
        data_bytes = data.encode("utf-8")
        self.blob_client.upload_blob(data_bytes, overwrite=True)

    def download(self) -> bytes:
        downloader = self.blob_client.download_blob()
        return downloader.readall()

    def blob_exists(self) -> bool:
        return self.blob_client.exists()
