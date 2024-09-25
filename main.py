import os

import requests
from dotenv import load_dotenv, set_key
from pandas import DataFrame, ExcelWriter

load_dotenv()

DOTENV_PATH = ".env"
KEY_API_USERNAME = "API_USERNAME"
KEY_API_PASSWORD = "API_PASSWORD"

if KEY_API_USERNAME not in os.environ:
    os.environ[KEY_API_USERNAME] = input("Username: ")
    set_key(DOTENV_PATH, KEY_API_USERNAME, os.environ[KEY_API_USERNAME])
if KEY_API_PASSWORD not in os.environ:
    os.environ[KEY_API_PASSWORD] = input("Password: ")
    set_key(DOTENV_PATH, KEY_API_PASSWORD, os.environ[KEY_API_PASSWORD])

payload = {
    "source": "google_search",
    "query": "pharmacogenomics",
    "geo_location": "Australia",
    "locale": "en-us",
    "parse": True,
    "start_page": 1,
    "pages": 2,
    "limit": 10,
}

response = requests.request(
    "POST",
    "https://realtime.oxylabs.io/v1/queries",
    auth=(os.environ[KEY_API_USERNAME], os.environ[KEY_API_PASSWORD]),
    json=payload,
)

pages = response.json()["results"]

organic_results = []
for page, data in enumerate(pages):
    for x in data["content"]["results"]["organic"]:
        i = (page * 10) + int(x["pos"])
        organic_results.append(
            {"pos": i, "url": x["url"], "title": x["title"], "desc": x["desc"]}
        )

df = DataFrame(organic_results)
with ExcelWriter("data/export.xlsx") as writer:
    df.to_excel(writer)
