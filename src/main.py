import requests

from src.constants import ercol_url
from src.repository.price_checker.price_checker import get_price


def main() -> None:
    price = get_price(ercol_url, requests.get)
    print(price)


"""
get price
if csv exists, add to current
else save to new
"""

if __name__ == "__main__":
    main()
