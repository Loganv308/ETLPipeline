from sqlalchemy import create_engine

user = ''
password = ''
host = ''
port = ''
database = ''

def createTable():
    with open(r'src\\queries\\createTable.sql', 'r') as file:
        content = file.read()
    
    print(content)

def createEngine():
    return create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
        user, password, host, port, database
    ))