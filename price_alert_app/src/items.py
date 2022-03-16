from src.constants import ERCOL_URL, TOASTER_URL
from src.models.models import Item

items = [
    Item(url=ERCOL_URL, description="ercol_bedside", scraper_marker="price price--large", scraper_trim=(1, 7)),
    Item(
        url=TOASTER_URL,
        description="dualit_toaster",
        scraper_marker="price price--large",
        scraper_trim=(1, 7),
    ),
]
