import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSettings:
    def __init__(self):
        self.DB_SERVER = os.getenv('DB_SERVER')
        self.DB_DATABASE = os.getenv('DB_DATABASE')
        self.DB_USERNAME = os.getenv('DB_USERNAME')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_DRIVER = os.getenv('DB_DRIVER')
    @property
    def db_connection_string(self):
        return f"Driver={self.DB_DRIVER};Server={self.DB_SERVER};Database={self.DB_DATABASE};User Id={self.DB_USERNAME};Password={self.DB_PASSWORD};"


class AppConfig:
    def __init__(self):
        self.database = DatabaseSettings()
        self.debug = os.getenv('DEBUG', 'False').lower() == "true"
    def validate(self):
        if not all([self.database.DB_SERVER, self.database.DB_DATABASE, self.database.DB_USERNAME, self.database.DB_PASSWORD, self.database.DB_DRIVER]):
            raise ValueError("Database configuration is incomplete.")