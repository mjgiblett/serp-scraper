import os

from dotenv import load_dotenv, set_key

from src.constants import DOTENV_PATH, KEY_API_PASSWORD, KEY_API_USERNAME


def init_env() -> None:
    load_dotenv()

    if KEY_API_USERNAME not in os.environ:
        os.environ[KEY_API_USERNAME] = input("Username: ")
        set_key(DOTENV_PATH, KEY_API_USERNAME, os.environ[KEY_API_USERNAME])
    if KEY_API_PASSWORD not in os.environ:
        os.environ[KEY_API_PASSWORD] = input("Password: ")
        set_key(DOTENV_PATH, KEY_API_PASSWORD, os.environ[KEY_API_PASSWORD])
