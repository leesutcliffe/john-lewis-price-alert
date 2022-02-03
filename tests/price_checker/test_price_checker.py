from datetime import datetime
from unittest import mock

import freezegun
import pandas as pd

from src.price_checker import price_checker
from src.price_checker.price_checker import get_previous_prices
from src.repository.datastore import DataStore

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/15.0 "
    "Safari/605.1.15 "
)


def test_it_returns_price_when_url_is_requested():
    test_url = "https://www.abc.com"
    headers = {"User-Agent": user_agent}

    def _get_content():
        with open("tests/price_checker/ercol_page.html", "rb") as f:
            content = f.read()
        return content

    class MockedResponse:
        def __init__(self):
            self.content = _get_content()

    mocked_response = MockedResponse()
    mocked_request = mock.Mock()
    mocked_request.get.return_value = mocked_response

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

    actual_df = price_checker.add_current_price_to_df(test_df, 450.0)
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

    actual_df = get_previous_prices(mocked_datastore)
    pd.testing.assert_frame_equal(test_df, actual_df)
