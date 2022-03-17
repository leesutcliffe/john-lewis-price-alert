import os

from sendgrid import Mail, SendGridAPIClient

from src.models.models import Item


def send(item: Item, previous_price: float, current_price: float) -> int:
    sendgrid_api_key = str(os.environ.get("SENDGRID_API_KEY"))
    message = Mail(
        from_email="lee@32mt.uk",
        to_emails="lee@32mt.uk",
        subject="Price Alert",
        html_content=f"{item.description} reduced from £{previous_price} to £{current_price}<br>{item.url}",
    )
    sg = SendGridAPIClient(sendgrid_api_key)
    response = sg.send(message)
    return response.status_code
