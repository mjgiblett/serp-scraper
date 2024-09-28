DOTENV_PATH = ".env"
KEY_API_USERNAME = "API_USERNAME"
KEY_API_PASSWORD = "API_PASSWORD"

DATA_PATH = "data/"
REQUEST_URL = "https://realtime.oxylabs.io/v1/queries"
REQUEST_PAYLOAD = {
    "source": "google_search",
    "query": "pizza",
    "geo_location": "Australia",
    "locale": "en-us",
    "parse": True,
    "start_page": 1,
    "pages": 2,
    "limit": 10,
}
