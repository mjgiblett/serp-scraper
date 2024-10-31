import os
import sys
from datetime import datetime
from glob import glob
from pathlib import Path

import click
from pandas import DataFrame, concat

from serps import __version__
from serps.config import get_user_config, save_user_config
from serps.constants import (
    API_OPTION_SOURCE,
    API_PASSWORD,
    API_USERNAME,
    DATAFRAME_COLUMNS,
    QUERIES_FILETYPE,
    QUERIES_PATH,
    RESULTS_PATH,
)
from serps.main import get_unique, load_list, request_scrape, save_excel, save_yaml


def version_msg() -> str:
    """Return serps version, location, and Python version."""
    python_version = sys.version
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f"SERP Scraper {__version__} from {location} (Python {python_version})"


def list_path(user_save_path: str, list_name: str) -> Path:
    return Path(user_save_path) / f"{list_name}{QUERIES_FILETYPE}"


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.pass_context
def cli(ctx) -> None:
    ctx.ensure_object(dict)
    config = get_user_config()
    if not config[API_USERNAME]:
        click.echo("Oxylabs API username missing.")
    if not config[API_PASSWORD]:
        click.echo("Oxylabs API password missing.")
    ctx.obj = config


@cli.command(help="Provide api username and password.")
@click.option(
    "--username",
    prompt=True,
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
)
@click.pass_context
def auth(ctx, username: str, password: str) -> None:
    ctx.obj[API_USERNAME] = username
    ctx.obj[API_PASSWORD] = password
    save_user_config(ctx.obj)


@cli.command(help="Scrape lists.")
@click.argument("lists", nargs=-1, required=True)
@click.option("-u", "--unique", is_flag=True, help="Return unique.")
@click.pass_context
def scrape(ctx, lists: tuple[str], unique: bool) -> None:
    auth = ctx.obj[API_USERNAME], ctx.obj[API_PASSWORD]
    df = DataFrame(columns=DATAFRAME_COLUMNS)
    for l in lists:
        path = list_path(ctx.obj[QUERIES_PATH], l)
        loaded = load_list(path)
        if not loaded:
            click.echo(f"Unable to load list {l}.")
            return
        click.echo(f"Requesting {l}...")
        data = request_scrape(auth, loaded)
        df = concat([df, data], ignore_index=True)
    conf_path = ctx.obj[RESULTS_PATH]
    file_path = f"{conf_path}{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.xlsx"
    save_excel(file_path, df)
    if unique:
        df_unique = get_unique(df)
        file_path = (
            f"{conf_path}{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}_unique.xlsx"
        )
        save_excel(file_path, df_unique)


@cli.command(help="Add query to specified list.")
@click.argument("list", required=True)
@click.argument(
    "keywords",
    required=True,
    nargs=-1,
)
@click.pass_context
def add(ctx, list: str, keywords: str) -> None:
    path = list_path(ctx.obj[QUERIES_PATH], list)
    loaded = load_list(path)
    if not loaded:
        click.echo(f"Unable to load list {list}.")
        return
    query = " ".join(keywords)
    loaded["queries"] = (*loaded["queries"], query)
    save_yaml(path, loaded)
    click.echo(f"Added query '{query}' to {list}.")


@cli.command(help="Lists all query list.")
@click.option("-f", "--full", is_flag=True, help="Show full file path.")
@click.pass_context
def ls(ctx, full: bool) -> None:
    path = ctx.obj[QUERIES_PATH]
    for x, yaml_file in enumerate(glob(f"{path}*{QUERIES_FILETYPE}")):
        if full:
            click.echo(f"{x} | {yaml_file}")
        else:
            click.echo(f"{x} | {Path(yaml_file).stem}")


@cli.command(help="Remove query from selected list.")
@click.argument("l", required=True)
@click.argument("query_number", type=int, required=True)
@click.pass_context
def remove(ctx, l: str, query_number: int) -> None:
    path = list_path(ctx.obj[QUERIES_PATH], l)
    loaded = load_list(path)
    if not loaded:
        click.echo(f"Unable to load list {l}.")
        return

    li = list(loaded["queries"])
    del li[query_number]

    loaded["queries"] = tuple(li)
    save_yaml(path, loaded)

    print(f"{query_number} removed from {l}!")


@cli.command(
    help="Create new query list.",
)
@click.argument("name")
@click.option(
    "-s",
    "--source",
    default="google_search",
    type=click.Choice(API_OPTION_SOURCE, case_sensitive=False),
    help="The scraper that will process your request.",
)
@click.option("-q", "--queries", multiple=True, help="Search term.")
@click.option(
    "-g",
    "--geo-location",
    default="Australia",
    help=(
        "Customises request based on geographic locations. "
        "Works differently depending on the website you're scraping."
    ),
)
@click.option(
    "-d",
    "--domain",
    default="com.au",
    help="Specifies which Amazon marketplace to scrape.",
)
@click.option(
    "-l",
    "--locale",
    default="en-au",
    help="Specifies the interface language.",
)
@click.option(
    "--parse/--no-parse",
    default=True,
    help="Request returns structured data.",
)
@click.option("--start-page", default=1, help="Starting page number.", type=int)
@click.option("--pages", default=1, help="Number of pages to scrape.", type=int)
@click.option(
    "--limit", default=10, help="Number of results to retrieve in each page.", type=int
)
@click.pass_context
def new(
    ctx,
    name: str,
    source: str,
    queries: tuple[str],
    geo_location: str,
    domain: str,
    locale: str,
    parse: bool,
    start_page: int,
    pages: int,
    limit: int,
) -> None:
    file_path = Path(ctx.obj[QUERIES_PATH]) / f"{name}.yaml"
    payload = {
        "source": source,
        "queries": queries,
        "geo_location": geo_location,
        "domain": domain,
        "locale": locale,
        "parse": parse,
        "start_page": start_page,
        "pages": pages,
        "limit": limit,
    }
    save_yaml(file_path, payload)


@cli.command(
    help="Delete query list.",
)
@click.argument("list", required=True)
@click.pass_context
def delete(ctx, list: str) -> None:
    path = list_path(ctx.obj[QUERIES_PATH], list)
    if not os.path.exists(path):
        return
    os.remove(path)
    click.echo(f"Deleted {list} at {path}.")


@cli.command(help="Show list.")
@click.argument("list", required=True)
@click.pass_context
def show(ctx, list) -> None:
    path = list_path(ctx.obj[QUERIES_PATH], list)
    loaded = load_list(path)
    if not loaded:
        click.echo(f"Unable to load list {list}.")
        return
    if len(loaded["queries"]) == 0:
        click.echo("No queries in list. Use 'add' command to add query.")
    for k, v in loaded.items():
        if type(v) is tuple:
            click.echo(k + ":")
            for x, t in enumerate(v):
                click.echo(f"   {x} | {t}")
        else:
            click.echo(f"{k}: {v}")


@cli.command(help="Rename query list.")
@click.argument("list", required=True)
@click.argument("new_name", required=True)
@click.pass_context
def rename(ctx, list: str, new_name: str) -> None:
    path = list_path(ctx.obj[QUERIES_PATH], list)
    loaded = load_list(path)
    if not loaded:
        click.echo(f"Unable to load list {list}.")
        return
    file_path = Path(ctx.obj[QUERIES_PATH]) / f"{new_name}.yaml"
    save_yaml(file_path, loaded)
    os.remove(path)
    click.echo(f"Renamed {list} to {new_name}.")
