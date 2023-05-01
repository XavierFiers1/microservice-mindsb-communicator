import os

import pymysql
from dotenv import load_dotenv


class DatabaseService():

    def __init__(self) -> None:
        load_dotenv()
        self.db = None

    def open_database_connection(self):
        self.db = pymysql.connect(
            host="cloud.mindsdb.com",
            user=os.environ.get("MINDSDB_USER"),
            password=os.environ.get("MINDSDB_PASSWORD"),
            port=3306,
        )

    def close(self):
        self.db.close()

    @property
    def database(self) -> any:
        return self.db
