from src.save import save
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

    save(organic_results)


if __name__ == "__main__":
    from src.environment import init_env

    init_env()
    main()
