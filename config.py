from dotenv import load_dotenv
import os

load_dotenv()  # подтягивает .env

API_TOKEN = os.getenv("API_TOKEN")
DB_PATH = os.getenv("DB_PATH")