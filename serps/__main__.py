"""Allow serps to be executable through `python -m serps`."""

from serps.cli import cli

if __name__ == "__main__":
    cli(prog_name="SERP Scraper")
