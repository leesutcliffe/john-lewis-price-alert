import os

import freezegun
import pytest

from price_alert_app.src.start import start
from price_alert_app.tests.conftest import AZURITE_STORAGE_CONNECTION

os.environ["STORAGE_CONNECTION"] = AZURITE_STORAGE_CONNECTION


@pytest.mark.integration
@freezegun.freeze_time("2022-01-01")
def test_data_is_saved_when_data_doesnt_exist(integration_clients, test_df_to_csv):
    blob_client = integration_clients["blob_client"]
    container_client = integration_clients["container_client"]

    start()

    download_stream = blob_client.download_blob()
    actual_csv_data = download_stream.readall()
    test_csv_data = test_df_to_csv.encode("utf-8")

    assert test_csv_data == actual_csv_data
    assert blob_client.blob_name == "prices.csv"

    # clean up
    blob_client.delete_blob()
    container_client.delete_container()


@pytest.mark.integration
@freezegun.freeze_time("2022-01-02")
def test_data_is_saved_when_existing_data_already_exists(
    integration_clients, test_df_to_csv, test_with_existing_df_to_csv
):
    blob_client = integration_clients["blob_client"]
    container_client = integration_clients["container_client"]

    # setup existing data
    test_csv_as_bytes = test_df_to_csv.encode("utf-8")
    blob_client.upload_blob(data=test_csv_as_bytes)

    start()

    download_stream = blob_client.download_blob()
    actual_downloaded_data = download_stream.readall()
    expected_downloaded_data = test_with_existing_df_to_csv.encode("utf-8")

    assert expected_downloaded_data == actual_downloaded_data
    assert blob_client.blob_name == "prices.csv"

    # clean up
    blob_client.delete_blob()
    container_client.delete_container()
