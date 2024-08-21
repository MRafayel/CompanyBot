import os
import json
from dotenv import load_dotenv

load_dotenv()

website_url = os.getenv("WEBSITE_URL")

headers = {
    'accept': os.getenv("ACCEPT"),
    'user-agent': os.getenv("USERAGENT"),
        }

category_url = os.getenv("CATEGORY_URL")

website_core = os.getenv("WEBSITE_CORE")

DATABASE_PATH = os.getenv("DATABASE_PATH")

FIELDS = json.loads(os.getenv("FIELDS"))

TOKEN = os.getenv("TOKEN")
