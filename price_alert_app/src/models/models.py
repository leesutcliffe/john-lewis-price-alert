from typing import Tuple

from pydantic import BaseModel


class Item(BaseModel):
    url: str
    description: str
    scraper_marker: str
    scraper_trim: Tuple[int, int]
