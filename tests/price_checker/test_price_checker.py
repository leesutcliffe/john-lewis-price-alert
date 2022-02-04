import os
from datetime import datetime
from unittest import mock

import freezegun
import pandas as pd

from src.constants import USER_AGENT
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore

test_url = "https://www.abc.com"
headers = {"User-Agent": USER_AGENT}


def get_content():
    file_path = os.getcwd()
    with open(f"{file_path}/tests/price_checker/ercol_page.html", "rb") as f:
        content = f.read()
    return content


class MockedResponse:
    def __init__(self):
        self.content = get_content()


def test_it_returns_price_when_url_is_requested():
    mocked_response = MockedResponse()
    mocked_request = mock.Mock()
    mocked_request.get.return_value = mocked_response
    mocked_datastore = mock.MagicMock(spec=DataStore)

    price_checker = PriceChecker(mocked_datastore)

    actual = price_checker.get_price(test_url, mocked_request.get)
    mocked_request.get.assert_called_with(test_url, headers=headers)
    assert actual == 450.00


@freezegun.freeze_time("2022-01-02")
def test_save_price_pandas_dataframe():
    test_data = {
        "Date": [datetime(2022, 1, 1)],
        "Price": [450.0],
    }
    test_df = pd.DataFrame(data=test_data).set_index("Date")
    test_expected = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 2)],
        "Price": [450.0, 450.0],
    }
    expected_df = pd.DataFrame(data=test_expected).set_index("Date")
    mocked_datastore = mock.MagicMock(spec=DataStore)
    price_checker = PriceChecker(mocked_datastore)

    actual_df = price_checker._add_current_price_to_df(test_df, 450.0)
    pd.testing.assert_frame_equal(expected_df, actual_df)


@freezegun.freeze_time("2022-01-02")
def test_get_previous_prices_as_dataframe():
    test_data = {
        "Date": [datetime(2022, 1, 1)],
        "Price": [450.0],
    }
    test_df = pd.DataFrame(data=test_data).set_index("Date")
    test_csv_as_bytes = bytes(test_df.to_csv(), "utf-8")

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.download.return_value = test_csv_as_bytes
    mocked_datastore.blob_exists.return_value = True

    price_checker = PriceChecker(mocked_datastore)

    actual_df = price_checker._get_previous_prices()
    pd.testing.assert_frame_equal(test_df, actual_df)


@freezegun.freeze_time("2022-01-02")
def test_save_price_as_dataframe_when_previous_prices_dont_exist():
    test_data = {
        "Date": [datetime(2022, 1, 2)],
        "Price": [450.0],
    }
    test_df = pd.DataFrame(data=test_data).set_index("Date")
    expected = test_df.to_csv()

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.blob_exists.return_value = False
    price_checker = PriceChecker(mocked_datastore)

    actual = price_checker._prepare_data(450.0)

    assert expected == actual


@freezegun.freeze_time("2022-01-01")
def test_update_prices_by_passing_csv_to_datastore_when_existing_data_does_not_exist():
    test_data = {
        "Date": [datetime(2022, 1, 1)],
        "Price": [450.0],
    }
    test_csv_data = pd.DataFrame(data=test_data).set_index("Date").to_csv()

    mocked_response = MockedResponse()
    mocked_request = mock.Mock()
    mocked_request.get.return_value = mocked_response
    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.save_data.return_value = None
    mocked_datastore.blob_exists.return_value = False

    # mocked_datastore.download.return_value = bytes(test_csv_data, "utf-8")

    price_checker = PriceChecker(mocked_datastore)

    price_checker.get_price(mocked_datastore, mocked_request.get, save_price=True)

    mocked_datastore.save_data.assert_called_once_with(test_csv_data)


@freezegun.freeze_time("2022-01-02")
def test_update_prices_by_passing_csv_to_datastore_when_existing_data_exists():
    test_data = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 2)],
        "Price": [450.0, 450.0],
    }
    test_csv_data = pd.DataFrame(data=test_data).set_index("Date").to_csv()

    test_existing_data = {
        "Date": [datetime(2022, 1, 1)],
        "Price": [450.0],
    }
    test_existing_data = pd.DataFrame(data=test_existing_data).set_index("Date").to_csv()

    mocked_response = MockedResponse()
    mocked_request = mock.Mock()
    mocked_request.get.return_value = mocked_response
    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.save_data.return_value = None
    mocked_datastore.blob_exists.return_value = True

    mocked_datastore.download.return_value = bytes(test_existing_data, "utf-8")

    price_checker = PriceChecker(mocked_datastore)

    price_checker.get_price(mocked_datastore, mocked_request.get, save_price=True)

    mocked_datastore.save_data.assert_called_once_with(test_csv_data)
