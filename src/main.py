import datetime
from collections.abc import Callable

import pandas as pd
import requests
from bs4 import BeautifulSoup

ercol_url = "https://www.johnlewis.com/" "ercol-for-john-lewis-shalstone-2-drawer-bedside-table/p2523085"
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


def save_current_price(df: pd.DataFrame, price: float) -> pd.DataFrame:
    new_row = pd.DataFrame({"Date": [datetime.datetime.now()], "Price": [price]})
    updated_df = pd.concat([df, new_row], ignore_index=True)
    return updated_df


def main() -> None:
    price = get_price(ercol_url, requests.get)
    print(price)


if __name__ == "__main__":
    main()
