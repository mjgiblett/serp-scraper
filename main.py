import os
from datetime import datetime

import requests
from pandas import DataFrame, ExcelWriter

from src.constants import DATA_PATH, KEY_API_PASSWORD, KEY_API_USERNAME, REQUEST_PAYLOAD
from src.environment import init_env


def main() -> None:
    init_env()

    response = requests.request(
        "POST",
        "https://realtime.oxylabs.io/v1/queries",
        auth=(os.environ[KEY_API_USERNAME], os.environ[KEY_API_PASSWORD]),
        json=REQUEST_PAYLOAD,
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
    writer_path = f"{DATA_PATH}{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.xlsx"
    with ExcelWriter(writer_path) as writer:
        df.to_excel(writer)


if __name__ == "__main__":
    main()
