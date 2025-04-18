import os 
from dotenv  import load_dotenv

load_dotenv(override=True)

# Database configuration file:
DB_CONFIG = {
    'dbname': os.getenv("dbname"),
    'user': os.getenv("user"),
    'password': os.getenv("password"),
    'host': os.getenv("host"),
    'port': os.getenv("port", "5432")
}

