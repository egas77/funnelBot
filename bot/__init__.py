import logging
import sys

from pyrogram import Client

from config import Config

file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8")
stdout_handler = logging.StreamHandler(sys.stdout)

logger = logging.getLogger('bot_logger')
if Config.DEBUG:
    logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

api_id = Config.API_ID
api_hash = Config.API_HASH
client_name = Config.CLIENT_NAME

app = Client(client_name, api_id, api_hash)

from .handlers import *
