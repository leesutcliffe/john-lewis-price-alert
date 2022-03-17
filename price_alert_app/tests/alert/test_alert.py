import os
import unittest
from unittest import mock

from src.alert import alert
from src.models.models import Item
from tests.conftest import TEST_URL


class MockedMail:
    def __init__(self, from_email, to_emails, subject, html_content):
        self.from_email = from_email
        self.to_emails = to_emails
        self.subject = subject
        self.html_content = html_content


class MockedSendResponse:
    status_code = 202


class MockedSendGrid:
    def __init__(self, api_key):
        self.api_key = api_key
        self.response = MockedSendResponse()

    def send(self, message):
        return self.response


class MailTest(unittest.TestCase):
    @mock.patch("src.alert.alert.SendGridAPIClient", side_effect=MockedSendGrid)
    @mock.patch("src.alert.alert.Mail", side_effect=MockedMail)
    def test_sending_email(self, mocked_mail, mocked_sendgrid):
        os.environ["SENDGRID_API_KEY"] = "12345"

        test_item = Item(url=TEST_URL, description="some_item")
        actual = alert.send(test_item, 500.0, 450.0)

        self.assertIn(
            mock.call(
                from_email="lee@32mt.uk",
                to_emails="lee@32mt.uk",
                subject="Price Alert",
                html_content=f"some_item reduced from £500.0 to £450.0<br>{TEST_URL}",
            ),
            mocked_mail.call_args_list,
        )
        self.assertIn(
            mock.call("12345"),
            mocked_sendgrid.call_args_list,
        )
        assert actual == 202
