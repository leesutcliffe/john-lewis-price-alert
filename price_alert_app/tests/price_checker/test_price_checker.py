import os
from datetime import datetime
from unittest import mock

import freezegun
import pandas as pd
import requests_mock

from src.constants import ERCOL_URL, USER_AGENT
from src.models.models import Item
from src.price_checker.price_checker import PriceChecker
from src.repository.datastore import DataStore

headers = {"User-Agent": USER_AGENT}

html_test_page = (
    os.path.abspath("ercol_page.html")
    if os.path.basename(os.getcwd()) == "price_checker"
    else os.path.abspath("tests/price_checker/ercol_page.html")
)


def get_content():
    with open(html_test_page, "rb") as f:
        content = f.read()
    return content


test_content = '<p class="price price--large">£450.00</p>'.encode("utf-8")

test_item = Item(url=ERCOL_URL, description="item_a", scraper_marker="price price--large", scraper_trim=(1, 7))


def test_it_returns_price_when_url_is_requested():
    mocked_datastore = mock.MagicMock(spec=DataStore)
    price_checker = PriceChecker(mocked_datastore)
    with requests_mock.Mocker(real_http=True) as req_mock:
        req_mock.register_uri("GET", ERCOL_URL, content=test_content)

        actual = price_checker.get_current_price(test_item)

    assert actual == 450.00


@freezegun.freeze_time("2022-01-02")
def test_save_price_pandas_dataframe():
    test_data = {"Date": [datetime(2022, 1, 1)], "Price": [450.0], "Item": ["item_a"]}
    test_df = pd.DataFrame(data=test_data).set_index("Item")
    test_expected = {"Date": [datetime(2022, 1, 2)], "Price": [450.0], "Item": ["item_a"]}
    expected_df = pd.DataFrame(data=test_expected).set_index("Item")
    mocked_datastore = mock.MagicMock(spec=DataStore)

    price_checker = PriceChecker(mocked_datastore)
    price_checker.description = "item_a"

    actual_df = price_checker._update_df(test_df, 450.0)
    pd.testing.assert_frame_equal(expected_df, actual_df)


@freezegun.freeze_time("2022-01-02")
def test_get_previous_prices_as_dataframe():
    test_data = {"Date": [datetime(2022, 1, 1)], "Price": [450.0], "Item": ["item_a"]}
    test_df = pd.DataFrame(data=test_data).set_index("Item")
    test_csv_as_bytes = bytes(test_df.to_csv(), "utf-8")

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.download.return_value = test_csv_as_bytes
    mocked_datastore.blob_exists.return_value = True

    price_checker = PriceChecker(mocked_datastore)

    actual_df = price_checker._get_previous_prices()
    pd.testing.assert_frame_equal(test_df, actual_df)


@freezegun.freeze_time("2022-01-02")
def test_save_price_as_dataframe_when_previous_prices_dont_exist():
    test_data = {"Date": [datetime(2022, 1, 2)], "Price": [450.0], "Item": ["item_a"]}
    test_df = pd.DataFrame(data=test_data).set_index("Item")
    expected = test_df.to_csv()

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.blob_exists.return_value = False

    price_checker = PriceChecker(mocked_datastore)
    price_checker.description = "item_a"

    actual = price_checker._prepare_data(450.0)

    assert expected == actual


@freezegun.freeze_time("2022-01-01")
def test_update_prices_by_passing_csv_to_datastore_when_existing_data_does_not_exist():
    test_data = {"Date": [datetime(2022, 1, 1)], "Price": [450.0], "Item": ["item_a"]}
    test_csv_data = pd.DataFrame(data=test_data).set_index("Item").to_csv()

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.save_data.return_value = None
    mocked_datastore.blob_exists.return_value = False

    price_checker = PriceChecker(mocked_datastore)
    price_checker.description = "item_a"
    price_checker.save_price(450.0)

    mocked_datastore.save_data.assert_called_once_with(test_csv_data)


@freezegun.freeze_time("2022-01-02")
def test_update_item_a_price_by_passing_csv_to_datastore_when_existing_data_exists():
    expected_test_data = {
        "Date": [datetime(2022, 1, 2), datetime(2022, 1, 1)],
        "Price": [450.0, 200],
        "Item": ["item_a", "item_b"],
    }
    expected_csv_data = pd.DataFrame(data=expected_test_data).set_index("Item").to_csv()

    test_existing_data = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 1)],
        "Price": [450.0, 200],
        "Item": ["item_a", "item_b"],
    }
    test_existing_data = pd.DataFrame(data=test_existing_data).set_index("Date").to_csv()

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.save_data.return_value = None
    mocked_datastore.blob_exists.return_value = True

    mocked_datastore.download.return_value = bytes(test_existing_data, "utf-8")

    price_checker = PriceChecker(mocked_datastore)
    with requests_mock.Mocker(real_http=True) as req_mock:
        req_mock.register_uri("GET", ERCOL_URL, content=test_content)
        price = price_checker.get_current_price(test_item)
        price_checker.save_price(price)

    mocked_datastore.save_data.assert_called_once_with(expected_csv_data)


@freezegun.freeze_time("2022-01-03")
def test_get_most_recent_previous_price():
    test_data = {
        "Date": [datetime(2022, 1, 1), datetime(2022, 1, 1)],
        "Price": [450.0, 200],
        "Item": ["item_a", "item_b"],
    }
    test_existing_data = pd.DataFrame(data=test_data).set_index("Item").to_csv()

    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.download.return_value = bytes(test_existing_data, "utf-8")

    price_checker = PriceChecker(mocked_datastore)
    price_checker.description = "item_a"

    actual = price_checker.previous_price()

    assert 450.0 == actual


@freezegun.freeze_time("2022-01-03")
def test_return_zero_if_no_previous_price():
    mocked_datastore = mock.MagicMock(spec=DataStore)
    mocked_datastore.blob_exists.return_value = False

    price_checker = PriceChecker(mocked_datastore)

    actual = price_checker.previous_price()

    assert 0 == actual
