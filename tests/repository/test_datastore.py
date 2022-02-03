from datetime import datetime
from unittest import mock

import pandas as pd
from azure.storage.blob import BlobClient, BlobServiceClient

from src.repository.datastore import DataStore

CONTAINER_NAME = "data"
BLOB_NAME = "ercol_prices.csv"


def test_data_is_uploaded_blob_storage():
    test_data = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 1)],
        "Price": [450.0, 450.0],
    }
    csv_data = pd.DataFrame(data=test_data).to_csv

    mocked_blob_svc_client = mock.MagicMock(spec=BlobServiceClient)
    mocked_blob_client = mock.MagicMock(spec=BlobClient)
    mocked_blob_client.upload_blob.return_value = None
    mocked_blob_svc_client.get_blob_client.return_value = mocked_blob_client

    datastore = DataStore(mocked_blob_svc_client, BLOB_NAME)
    datastore.save_data(csv_data)

    mocked_blob_svc_client.get_blob_client.assert_called_once_with(CONTAINER_NAME, BLOB_NAME)
    mocked_blob_client.upload_blob.assert_called_once_with(csv_data, overwrite=True)


def test_download_csv_from_blob_storage():
    mocked_blob_svc_client = mock.MagicMock(spec=BlobServiceClient)
    mocked_blob_client = mock.MagicMock(spec=BlobClient)
    mocked_blob_svc_client.get_blob_client.return_value = mocked_blob_client

    datastore = DataStore(mocked_blob_svc_client, BLOB_NAME)
    datastore.download()
    mocked_blob_client.download_blob.assert_called()


def test_returns_false_if_blob_doesnt_exist():
    mocked_blob_svc_client = mock.MagicMock(spec=BlobServiceClient)
    mocked_blob_client = mock.MagicMock(spec=BlobClient)
    mocked_blob_svc_client.get_blob_client.return_value = mocked_blob_client
    mocked_blob_client.exists.return_value = False

    datastore = DataStore(mocked_blob_svc_client, BLOB_NAME)
    result = datastore.blob_exists()

    assert result is False


def test_returns_false_if_blob_does_exist():
    mocked_blob_svc_client = mock.MagicMock(spec=BlobServiceClient)
    mocked_blob_client = mock.MagicMock(spec=BlobClient)
    mocked_blob_svc_client.get_blob_client.return_value = mocked_blob_client
    mocked_blob_client.exists.return_value = True

    datastore = DataStore(mocked_blob_svc_client, BLOB_NAME)
    result = datastore.blob_exists()

    assert result is True
