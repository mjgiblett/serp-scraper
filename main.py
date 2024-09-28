from datetime import datetime

from pandas import DataFrame, ExcelWriter

from src.constants import DATA_PATH
from src.scrape import scrape_pages


def main() -> None:
    pages = scrape_pages()

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
    from src.environment import init_env

    init_env()
    main()
