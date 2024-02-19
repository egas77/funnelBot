import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)
load_dotenv(os.path.join(os.getcwd(), '.env.local'), override=True)


class Config(object):
    USERNAME = os.getenv("USERNAME")
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    CLIENT_NAME = os.getenv("CLIENT_NAME")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEBUG = bool(int(os.getenv("DEBUG")))
    SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL"))
