import pyodbc
import os
import sys  
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config.settings import AppConfig


def test_db_connection():
    config = AppConfig()
    print(f"Connection string: {config.database.db_connection_string}")
    try:
        conn = pyodbc.connect(config.database.db_connection_string)
        # conn = pyodbc.connect(
        #         f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        #         f"SERVER={config.database.DB_SERVER};"
        #         f"DATABASE={config.database.DB_DATABASE};"
        #         f"UID={config.database.DB_USERNAME};"
        #         f"PWD={config.database.DB_PASSWORD}"
        #     )
        print(f"[INFO]: Successful Connection...")
        print(f"[SERVER]: {config.database.DB_SERVER}")
        print(f"[DATABASE]:{config.database.DB_DATABASE}")   
        conn.close()
        return True
    except pyodbc.Error as e:
        print(f"[ERROR] Connection Failure: {str(e)}")
        return False


if __name__=="__main__":
    test_db_connection()

    

