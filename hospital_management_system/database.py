import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("Database Connected Successfully")
            return connection

    except mysql.connector.Error as e:
        print("Database Error:", e)
        return None