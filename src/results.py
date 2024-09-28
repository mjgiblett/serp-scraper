def extract_results(pages: list) -> list:
    results = []
    for page, data in enumerate(pages):
        for result in data["content"]["results"]["organic"]:
            results.append(
                {
                    "Page": page,
                    "Position": result["pos"],
                    "URL": result["url"],
                    "Title": result["title"],
                    "Description": result["desc"],
                }
            )

    return results
