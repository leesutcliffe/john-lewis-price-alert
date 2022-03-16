from src.models.models import Item


def test_items():
    item = Item(
        url="https://some-path", description="Some Item", scraper_marker="price price--large", scraper_trim=(1, 7)
    )
    expected = dict(
        url="https://some-path", description="Some Item", scraper_marker="price price--large", scraper_trim=(1, 7)
    )

    actual = item.dict()
    assert actual == expected
