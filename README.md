# Price Alert

Price Alert is a Python project that sends an email alert (via SendGrid) when a tracked item at a chosen retailer is reduced. 

It runs daily on an Azure Function app, scrapes the price and stores it in a CSV file on an Azure Storage account. If the current price is lower than the previsouly recorded price, an email alert is generated 