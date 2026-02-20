from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

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

def readSQLScript(path: str) -> str:
    with open(path, 'r') as file:
        content = file.read()
    return content

def createEngine():
    port = int(get_required_env("DB_PORT"))

    connection_url = URL.create(
        drivername="mssql+pyodbc",
        username=get_required_env("DB_USER"),
        password=get_required_env("DB_PASSWORD"),
        host=get_required_env("DB_HOST"),
        port=port,
        database=get_required_env("DATABASE"),
        # Make sure to include these! Driver is necessary for pyodbc. 
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            # Sometimes necessary if connection doesn't work off the bat.
            "TrustServerCertificate": "yes"
        }
    )

    # Creates the engine using previous arguments. 
    engine = create_engine(
        connection_url,
        # True only for debugging
        echo=True          
    )

    # Returns the engine once called
    return engine

