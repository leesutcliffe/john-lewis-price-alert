from typing import Tuple

from pydantic import BaseModel

from src.constants import ERCOL_URL


class Item(BaseModel):
    url: str
    description: str
    scraper_marker: str
    scraper_trim: Tuple[int, int]


item = Item(url=ERCOL_URL, description="Ercol Bedside Table", scraper_marker="price price--large", scraper_trim=(1, 7))
