import os
from datetime import datetime
from typing import List

import pandas as pd
import pytest
from azure.storage.blob import BlobServiceClient

from src.models.models import Item

AZURITE_DEFAULT_KEY = (
    "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="  # noqa E501
)

AZURITE_STORAGE_CONNECTION = (
    f"DefaultEndpointsProtocol=http;"
    f"AccountName=devstoreaccount1;"
    f"AccountKey={AZURITE_DEFAULT_KEY};"
    f"BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

TEST_URL = "http://test.com"


@pytest.fixture
def integration_clients() -> dict:
    os.environ["CONTAINER_NAME"] = "data"
    blob_service_client = BlobServiceClient.from_connection_string(AZURITE_STORAGE_CONNECTION)

    container_client = blob_service_client.get_container_client("data")
    container_client.create_container()

    blob_client = blob_service_client.get_blob_client("data", "prices.csv")

    return {"container_client": container_client, "blob_client": blob_client}


@pytest.fixture
def test_df_to_csv() -> pd.DataFrame:
    test_data = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 1)],
        "Price": [450.0, 450.0],
        "Item": ["item_a", "item_b"],
    }
    return pd.DataFrame(data=test_data).set_index("Item").to_csv()


@pytest.fixture
def test_df_updated_to_csv() -> pd.DataFrame:
    test_data = {
        "Date": [datetime(2022, 1, 2), datetime(2022, 1, 2)],
        "Price": [450.0, 450.0],
        "Item": ["item_a", "item_b"],
    }
    return pd.DataFrame(data=test_data).set_index("Item").to_csv()


@pytest.fixture
def test_items() -> List[Item]:
    item_a = Item(url=TEST_URL, description="item_a")
    item_b = Item(url=TEST_URL, description="item_b")
    return [item_a, item_b]
