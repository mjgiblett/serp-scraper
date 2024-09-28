from src import extract_results, init_env, save, scrape_pages


def main() -> None:
    pages = scrape_pages()
    results = extract_results(pages)
    save(results)


if __name__ == "__main__":
    init_env()
    main()
