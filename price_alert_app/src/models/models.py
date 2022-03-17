from pydantic import BaseModel


class Item(BaseModel):
    url: str
    description: str
    scraper_marker = "price price--large"
    scraper_trim = (1, 7)
