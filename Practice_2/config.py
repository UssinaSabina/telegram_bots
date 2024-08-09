import os
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    config.get("bot", "token", fallback=None)
)

if not BOT_TOKEN:
    exit("please provide BOT_TOKEN env variable")

DOGS_PIC_URL = "https://klike.net/uploads/posts/2023-04/1681880659_3-71.jpg"
