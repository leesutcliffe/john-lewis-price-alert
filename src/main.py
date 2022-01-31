import requests

from src.repository.price_checker.price_checker import get_price

ercol_url = "https://www.johnlewis.com/" "ercol-for-john-lewis-shalstone-2-drawer-bedside-table/p2523085"


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
