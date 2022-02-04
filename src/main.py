import requests

from src.constants import ERCOL_URL
from src.price_checker.price_checker import PriceChecker


def main() -> None:
    price = PriceChecker()
    price = price.get_price(ERCOL_URL, requests.get)
    print(price)


"""
get price
if csv exists, add to current
else save to new
"""

if __name__ == "__main__":
    main()
