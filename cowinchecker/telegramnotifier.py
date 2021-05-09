import os

import requests


class CowinCheckerTelegramBot:
    CHANNEL_ID = os.environ.get("COWIN_CHECKER_TELEGRAM_CHANNEL_ID")
    BOT_TOKEN = os.environ.get("COWIN_CHECKER_TELEGRAM_BOT_TOKEN")
    API_BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
    MAX_TIMEOUT_SEC = 10

    @classmethod
    def send_notification(cls, text):
        API_URL = cls.API_BASE_URL + "/sendMessage"
        query_params = {
            "chat_id": cls.CHANNEL_ID,
            "text": text
        }
        response = requests.post(API_URL, params=query_params,
                                 timeout=cls.MAX_TIMEOUT_SEC)
        response.raise_for_status()
