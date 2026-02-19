from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port_str = os.environ.get("DB_PORT")
database = os.environ.get('DATABASE')

def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

def createTable():
    with open(r'src\\queries\\createTable.sql', 'r') as file:
        content = file.read()

def createEngine():
    port = int(get_required_env("DB_PORT"))

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=get_required_env("DB_USER"),
        password=get_required_env("DB_PASSWORD"),
        host=get_required_env("DB_HOST"),
        port=port,
        database=get_required_env("DATABASE"),
    )

    engine = create_engine(
        connection_url,
        pool_pre_ping=True,      # avoids stale connections
        pool_size=5,             # adjustable
        max_overflow=10,
        echo=False               # True only for debugging
    )

    logger.info("Database engine created successfully")

    return engine
