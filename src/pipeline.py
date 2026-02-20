from sqlalchemy import text
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import database
import os

# Loads .env file
load_dotenv()

# Global variables
CHUNK_SIZE = 500

# SQL Scripts
CREATETABLESCRIPT = r"src\queries\createTable.sql"
INSERTDATASCRIPT = r"src\queries\insertValues.sql"

# First and foremost, extract the data and load it into a pandas dataframe.
def extractData(filePath: str) -> pd.DataFrame:
    data = pd.read_csv(filePath, sep="\\t", dtype=str, na_values="\\N", header=None, names=["webid", "username", "email", "ip1", "ip2", "passhash"],)

    # Returns extracted data as a Dataframe.
    return data

# Drops Empty cells (if applicable) and otherwise formats pertaining data.
def transformData(data: pd.DataFrame) -> pd.DataFrame:
    # Drops NA rows
    data.dropna(how="all", inplace=True)

    # Drops duplicates if there are any.
    data.drop_duplicates(inplace=True)

    # Transforms variables columns to strip away any leading whitespace. 
    data["WebID"] = data["WebID"].str.strip()
    data["Username"] = data["Username"].str.strip()
    data["Email"] = data["Email"].str.strip()
    data["Passhash"] = data["Passhash"].str.strip()

    # Will replace all "NaN" values with "NULL" instead.
    data.replace({np.nan: None})

    # Returns the newly transformed data. (Dataframe)
    return data

# Grabs basic info from the dataframe.
def getDataInfo(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframeInfo = dataframe.info()

    return dataframeInfo

# Outputs data to new CSV
def outputData(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.to_csv(r"data\new_sample_data.csv", index=False)

if __name__ == "__main__":
    try:
        # Calls createEngine() function from database class
        engine = database.createEngine()
        
        # Printing for User to show it successfully connected with defined ENV variables.        
        print(f"Connection to the {os.environ.get('DB_HOST')} for user {os.environ.get('DB_USER')} created successfully.")

        # Extracts data into a dataframe
        data = extractData(r"data\sample_data.csv")

        # The "T" in "ETL", strips any string variables and nullifies data when necessary.
        transformedData = transformData(data)

        dataframeInfo = getDataInfo(data)

        # Enable if you'd like to output the data into a CSV (Not really necessary)
        # outputData(transformedData)
        
        # Reads Table SQL script
        tableCreation = database.readSQLScript(CREATETABLESCRIPT)

        # Reads insert SQL script
        tableInsert = database.readSQLScript(INSERTDATASCRIPT)

        # Converts transformedData (dataframe) into a dictionary
        records = transformedData.to_dict(orient="records")

        # Calculates chunk size when loading into database.
        num_chunks = len(records) // CHUNK_SIZE + (len(records) % CHUNK_SIZE > 0)

        # Using .begin() here ensures commit/rollback automatically.
        with engine.begin() as conn:

            # Executes table creation
            conn.execute(text(tableCreation))
            
            # For i in range of the number of chunks...
            for i in range(num_chunks):
                # Slice the full records list into a chunk of CHUNK_SIZE for batch insertion
                chunk = records[i*CHUNK_SIZE : (i+1)*CHUNK_SIZE]
                # For each row in the chunk list...
                for row in chunk:
                    # Executes query on each row that's in the database.
                    conn.execute(text(tableInsert), row)
                    print(f"Inserted chunk {i+1} / {num_chunks}") 

        print("CSV loaded in successfully!")

    except ValueError as e:
        raise ValueError(f"Invalid database configuration: {e}") from e
    except Exception as e:
        raise Exception(f"Other error: {e}") from e