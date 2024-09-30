from os import path
from pathlib import Path

# user config

API_USERNAME = "oxylabs_api_username"
API_PASSWORD = "oxylabs_api_password"
RESULTS_PATH = "results_path"
QUERIES_PATH = "queries_path"

USER_CONFIG_PATH = Path(path.expanduser("~/.config/serps/serpsrc"))

DOCUMENT_DIR_NAME = "SERP Scraper"

DEFAULT_CONFIG = {
    API_USERNAME: None,
    API_PASSWORD: None,
    RESULTS_PATH: path.expanduser(f"~/Documents/{DOCUMENT_DIR_NAME}/Results/"),
    QUERIES_PATH: path.expanduser(f"~/Documents/{DOCUMENT_DIR_NAME}/Queries/"),
}

# oxylabs api
# https://developers.oxylabs.io/scraper-apis/web-scraper-api

REQUEST_URL = "https://realtime.oxylabs.io/v1/queries"
API_OPTION_SOURCE = [
    "amazon_product",
    "amazon_search",
    "amazon_pricing",
    "amazon_sellers",
    "amazon_bestsellers",
    "amazon_reviews",
    "amazon_questions",
    "google_search",
    "google_ads",
    "google_images",
    "google_lens",
    "google_maps",
    "google_travel_hotels",
    "google_suggest",
    "google_trends_explore",
    "google_shopping_product",
    "google_shopping_search",
    "google_shopping_pricing",
    "bing_search",
]

# other

DATAFRAME_COLUMNS = ["Query", "Page", "Position", "URL", "Title", "Description"]
QUERIES_FILETYPE = ".yaml"
