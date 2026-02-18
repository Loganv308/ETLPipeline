import pandas as pd

# First and foremost, extract the data and load it into a pandas dataframe.
def extractData(filePath: str) -> str:
    data = pd.read_csv(filePath, sep="\\t", dtype=str, na_values="\\N", header=None, names=["WebID", "Username", "Email", "IP1", "IP2", "Passhash"],)
    
    loadedData = pd.DataFrame(data)

    return loadedData

# Drops Empty cells (if applicable) and otherwise formats pertaining data.
def transformData(data: pd.DataFrame) -> pd.DataFrame:
    data.dropna(how="all", inplace=True)

    data.drop_duplicates(inplace=True)

    #data["WebID"] = data["WebID"].astype(int)

    return data

# Grabs basic info from the dataframe.
def getDataInfo(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframeInfo = dataframe.info()

    return dataframeInfo

# Outputs data to new CSV
def outputData(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe.to_csv(r"data\newSample_data.csv", index=False)

if __name__ == "__main__":
    try:
        data = extractData(r"data\sample_data.csv")

        transformedData = transformData(data)

        dataframeInfo = getDataInfo(data)
        print(dataframeInfo)
        print(data.head())

        outputData(transformedData)
    except Exception as e:
        print(e)