import requests  # mypy: noqa
from django.conf import settings

LOGIN = settings.PLAYMOBILE_LOGIN
PASSWORD = settings.PLAYMOBILE_PASSWORD


def send_sms(phone_number: str, message: str):
    if not LOGIN or not PASSWORD:
        return
    data = {
        "messages":
            [
                {
                    "recipient": phone_number,
                    "message-id": "1as12123",

                    "sms": {

                        "originator": "Lalu",
                        "content": {
                            "text": message
                        }
                    }
                }
            ]
    }

    requests.post('https://send.smsxabar.uz/broker-api/send',
                  json=data,
                  auth=(
                      LOGIN.encode('utf-8'), PASSWORD.encode('utf-8')))
