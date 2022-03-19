### items.py
List of items tracked by the price checker app. 
The `Item` class has defaults to work with John Lewis, however any retailer can be used. 
Modify `scraper_marker` to reference the relevant HTML DOM/Class where the price is located. 
`scraper_trim` is a Tuple that trims any erroneous characters to the left and right of the price

```
class Item(BaseModel):
    url: str
    description: str
    scraper_marker = "price price--large"
    scraper_trim = (1, 7)```