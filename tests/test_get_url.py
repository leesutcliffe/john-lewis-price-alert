import datetime
from unittest import mock

import freezegun
import pandas as pd

import src.main as scraper

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/15.0 "
    "Safari/605.1.15 "
)


def test_it_returns_price_when_url_is_requested():
    test_url = "https://www.abc.com"
    headers = {"User-Agent": user_agent}

    def _get_content():
        with open("tests/config/ercol_page.html", "rb") as f:
            content = f.read()
        return content

    class MockedResponse:
        def __init__(self):
            self.content = _get_content()

    mocked_response = MockedResponse()
    mocked_request = mock.Mock()
    mocked_request.get.return_value = mocked_response

    actual = scraper.get_price(test_url, mocked_request.get)
    mocked_request.get.assert_called_with(test_url, headers=headers)
    assert actual == 450.00


@freezegun.freeze_time("2022-01-02")
def test_save_price_pandas_dataframe():
    test_data = {
        "Date": [datetime.datetime(2022, 1, 1)],
        "Price": [450.0],
    }
    test_df = pd.DataFrame(data=test_data)
    test_expected = {
        "Date": [datetime.datetime(2022, 1, 1), datetime.datetime(2022, 1, 2)],
        "Price": [450.0, 450.0],
    }
    expected_df = pd.DataFrame(data=test_expected)

    actual_df = scraper.save_current_price(test_df, 450.0)
    pd.testing.assert_frame_equal(expected_df, actual_df)
