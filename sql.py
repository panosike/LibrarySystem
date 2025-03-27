import mysql.connector 
from credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

#Creating and returning DB connection 
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )