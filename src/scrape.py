import os

import requests

from src.constants import (
    KEY_API_PASSWORD,
    KEY_API_USERNAME,
    REQUEST_PAYLOAD,
    REQUEST_URL,
)


def scrape_pages() -> list:
    response = requests.request(
        method="POST",
        url=REQUEST_URL,
        auth=(os.environ[KEY_API_USERNAME], os.environ[KEY_API_PASSWORD]),
        json=REQUEST_PAYLOAD,
    )

    return response.json()["results"]
