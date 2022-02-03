import datetime
import io
from collections.abc import Callable

import pandas as pd
from bs4 import BeautifulSoup

from src.repository.datastore import DataStore

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/15.0 "
    "Safari/605.1.15 "
)
headers = {"User-Agent": user_agent}


def get_price(ercol_url: str, get: Callable) -> float:
    response = get(ercol_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.find_all(class_="price price--large")
    item_price = tags[0].string[1:7]
    return float(item_price)


def add_current_price_to_df(df: pd.DataFrame, price: float) -> pd.DataFrame:
    new_row = pd.DataFrame({"Date": [datetime.datetime.now()], "Price": [price]}).set_index("Date")
    updated_df = pd.concat([df, new_row])
    return updated_df


def get_previous_prices(datastore: DataStore) -> pd.DataFrame:
    previous_prices = datastore.download()
    csv_file = io.StringIO(previous_prices.decode())
    previous_prices_df = pd.read_csv(csv_file, index_col="Date", parse_dates=["Date"])
    return previous_prices_df
