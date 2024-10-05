import dotenv
import os

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN", default="None")
ADMIN = int(os.getenv("ADMIN", default="None"))
DB_NAME = os.getenv("DB_NAME", default="None")
DB_USER = os.getenv("DB_USER", default="None")
DB_PASS = os.getenv("DB_PASS", default="None")
DB_HOST = os.getenv("DB_HOST", default="None")
DB_PORT = os.getenv("DB_PORT", default="None")