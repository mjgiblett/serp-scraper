import os
from pathlib import Path
from typing import Any

import requests
import yaml
from pandas import DataFrame, ExcelWriter, concat

from serps.constants import DATAFRAME_COLUMNS

REQUEST_URL = "https://realtime.oxylabs.io/v1/queries"


def mkdirs(file_path: Path | str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def save_yaml(file_path: Path | str, payload: dict[str, Any]) -> None:
    mkdirs(file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(payload, file, default_flow_style=False, sort_keys=False)


def save_excel(file_path: Path | str, data: DataFrame) -> None:
    mkdirs(file_path)
    with ExcelWriter(file_path) as writer:
        data.to_excel(writer)


def load_list(file_path: Path | str) -> dict[str, Any] | None:
    if not file_path:
        return
    if not os.path.exists(file_path):
        return
    with open(file_path, encoding="utf-8") as file:
        try:
            yaml_vars = yaml.load(file, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            msg = f"Unable to parse YAML file {file_path}."
            raise Exception(msg) from e
        if not isinstance(yaml_vars, dict):
            msg = f"Top-level element of YAML file {file_path} should be an object."
            raise Exception(msg)
    try:
        return yaml_vars
    except Exception as e:
        msg = f"Unable to load YAML file {file_path}."
        raise Exception(msg) from e


def request_scrape(auth: tuple[str, str], payload: dict[str, Any]) -> DataFrame:
    df = DataFrame(columns=DATAFRAME_COLUMNS)
    queries = payload["queries"]
    payload.pop("queries")
    for query in queries:
        payload["query"] = query
        response = requests.request(
            method="POST",
            url=REQUEST_URL,
            auth=auth,
            json=payload,
        )
        pages = response.json().get("results", [])
        results = []
        for page, data in enumerate(pages):
            for result in data["content"]["results"]["organic"]:
                results.append(
                    {
                        "Query": query,
                        "Page": page + 1,
                        "Position": result["pos"],
                        "URL": result["url"],
                        "Title": result["title"],
                        "Description": result["desc"],
                    }
                )
            df = concat([df, DataFrame(results)], ignore_index=True)

    return df
