import datetime
import io
from collections.abc import Callable

import pandas as pd
from bs4 import BeautifulSoup

from price_alert_app.src.constants import USER_AGENT
from price_alert_app.src.repository.datastore import DataStore


class PriceChecker:
    datastore: DataStore

    def __init__(self, datastore: DataStore):
        self.datastore = datastore

    def get_price(self, url: str, get: Callable, save_price: bool = False) -> float:
        response = get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(response.content, "html.parser")
        tags = soup.find_all(class_="price price--large")
        item_price = float(tags[0].string[1:7])
        if save_price:
            df = self._prepare_data(item_price)
            self.datastore.save_data(df)

        return item_price

    def _add_current_price_to_df(self, df: pd.DataFrame, price: float) -> pd.DataFrame:
        new_row = pd.DataFrame({"Date": [datetime.datetime.now()], "Price": [price]}).set_index("Date")
        updated_df = pd.concat([df, new_row])
        return updated_df

    def _get_previous_prices(self) -> pd.DataFrame:
        previous_prices = self.datastore.download()
        csv_file = io.StringIO(previous_prices.decode())
        previous_prices_df = pd.read_csv(csv_file, index_col="Date", parse_dates=["Date"])
        return previous_prices_df

    def _prepare_data(self, price: float) -> str:
        def _build_df() -> pd.DataFrame:
            if self.datastore.blob_exists():
                previous_prices_df = self._get_previous_prices()
                return self._add_current_price_to_df(previous_prices_df, price)
            else:
                data = {"Date": [datetime.datetime.now()], "Price": price}
                return pd.DataFrame(data=data).set_index("Date")

        prepared_data = _build_df()
        return prepared_data.to_csv()
