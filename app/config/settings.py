import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSettings:
    """
    Database configuration settings.

    This class provides a way to set the database connection
    settings.

    Attributes:
        DB_SERVER (str): The database server address.
        DB_DATABASE (str): The database name.
        DB_USERNAME (str): The user name to use when connecting to the database.
        DB_PASSWORD (str): The password to use when connecting to the database.
        DB_DRIVER (str): The ODBC driver to use when connecting to the database.
    """

    def __init__(self):
        """
        Initialize the database settings from environment variables.
        """
        self.DB_SERVER = os.getenv('DB_SERVER')
        self.DB_DATABASE = os.getenv('DB_DATABASE')
        self.DB_USERNAME = os.getenv('DB_USERNAME')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_DRIVER = os.getenv('DB_DRIVER')


    @property
    def db_connection_string(self) -> str:
        """SQLAlchemy-compatible connection string for SQL Server"""
        return (
            f"mssql+pyodbc://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@localhost:1433/{self.DB_DATABASE}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
            "&TrustServerCertificate=yes"
            "&Encrypt=no"
            "&authentication=SqlPassword"
        )


class AppConfig:
    """
    Application configuration class.

    This class stores the database configuration and
    other app settings.

    Attributes:
        database (DatabaseSettings): Database configuration.
        debug (bool): Debug mode.
    """

    def __init__(self):
        self.database = DatabaseSettings()
        self.debug = os.getenv('DEBUG', 'False').lower() == "true"

    def validate(self):
        """
        Validate the database configuration.

        Raises:
            ValueError: If any of the database configuration values are missing.
        """
        if not all([self.database.DB_SERVER, self.database.DB_DATABASE, self.database.DB_USERNAME, self.database.DB_PASSWORD, self.database.DB_DRIVER]):
            raise ValueError("Database configuration is incomplete.")