import datetime
import io

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.constants import USER_AGENT
from src.items import Item
from src.repository.datastore import DataStore


class PriceChecker:
    datastore: DataStore
    sendgrid_api_key: str
    current_price: float
    description: str

    def __init__(self, datastore: DataStore):
        self.datastore = datastore

    def get_current_price(self, item: Item) -> float:
        self.description = item.description
        response = requests.get(item.url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(response.content, "html.parser")
        tags = soup.find_all(class_=item.scraper_marker)
        left_slice = item.scraper_trim[0]
        right_slice = item.scraper_trim[1]
        item_price = float(tags[0].string[left_slice:right_slice])
        self.current_price = item_price
        return self.current_price

    def save_price(self, item_price: float) -> None:
        df = self._prepare_data(item_price)
        self.datastore.save_data(df)

    def previous_price(self) -> float:
        if self.datastore.blob_exists():
            previous_prices_df = self._get_previous_prices()
            most_recent_price = previous_prices_df.at[self.description, "Price"]
            return most_recent_price
        return 0

    def _update_df(self, df: pd.DataFrame, price: float) -> pd.DataFrame:
        df.loc[self.description, ["Date", "Price"]] = [datetime.datetime.now(), price]
        return df

    def _get_previous_prices(self) -> pd.DataFrame:
        previous_prices = self.datastore.download()
        csv_file = io.StringIO(previous_prices.decode())
        previous_prices_df = pd.read_csv(csv_file, index_col="Item", parse_dates=["Date"])
        return previous_prices_df

    def _prepare_data(self, price: float) -> str:
        def _build_df() -> pd.DataFrame:
            if self.datastore.blob_exists():
                previous_prices_df = self._get_previous_prices()
                return self._update_df(previous_prices_df, price)
            else:
                data = {"Date": [datetime.datetime.now()], "Price": price, "Item": self.description}
                return pd.DataFrame(data=data).set_index("Item")

        prepared_data = _build_df()
        return prepared_data.to_csv()
