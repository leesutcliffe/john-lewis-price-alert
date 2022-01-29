from datetime import datetime
from unittest import mock

import pandas as pd
from azure.storage.blob import BlobClient, BlobServiceClient

from src.repository.datastore import DataStore


def test_data_is_uploaded_blob_storage():
    test_data = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 1)],
        "Price": [450.0, 450.0],
    }
    csv_data = pd.DataFrame(data=test_data).to_csv

    mocked_blob_svc_client = mock.MagicMock(spec=BlobServiceClient)
    mocked_blob_client = mock.MagicMock(spec=BlobClient)
    mocked_blob_svc_client.get_blob_client.return_value = mocked_blob_client

    datastore = DataStore(mocked_blob_svc_client)
    datastore.save_data(csv_data)

    mocked_blob_svc_client.get_blob_client.assert_called_once_with("data", "ercol_prices.csv")
