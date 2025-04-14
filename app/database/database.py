from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from app.config.settings import AppConfig
import threading
from sqlalchemy import inspect
from app.models.models import *
from app.database.base import Base

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.config = AppConfig()
            self.engine = None
            self.SessionLocal = None
            self.Base = Base
            self.Base.metadata = Base.metadata
            self._is_initialized = False

    @property
    def is_initialized(self):
        """Check if the database manager has been initialized."""
        return self._is_initialized and self.engine is not None and self.SessionLocal is not None


    def initialize(self):
        if self._is_initialized:  # Use the protected attribute
            return

        # Create engine
        self.engine = create_engine(
            self.config.database.db_connection_string,
            pool_pre_ping=True,
            echo=True
        )

        # Create session factory
        session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        self.SessionLocal = scoped_session(session_factory)
        
        # Bind the base metadata to the engine
        self.Base.metadata.bind = self.engine
        self._is_initialized = True  # Update the protected attribute
    


    def create_tables(self):
        """Create all the tables in the database."""
        if not self.is_initialized:  # Check if the database manager has been initialized
            self.initialize()  # Initialize the database manager if it has not been initialized
        # temp_check.py
        print(f"Creating tables: {self.Base.metadata.tables.keys()}")

        self.Base.metadata.create_all(self.engine, checkfirst=False)

    def table_exists(self, table_name):
        """Check if a table exists in the database.
        
        Parameters
        ----------
        table_name : str
            The name of the table to check.
        
        Returns
        -------
        bool
            True if the table exists, False otherwise.
        """
        inspector = inspect(self.engine)  # Get a database inspector object
        return inspector.has_table(table_name)  # Check if the table exists

    @contextmanager
    def session_scope(self):
        """
        Provide a transactional scope for a session.

        The session is automatically committed if no exception is raised.
        If an exception is raised, the session is rolled back.

        :return: A context manager session object
        """
        if not self.is_initialized:
            self.initialize()  # Initialize the database manager if it has not been initialized
        session = self.SessionLocal()  # Create a new session object
        try:
            yield session  # Yield the session object
            session.commit()  # Commit the session if no exception is raised
        except:
            session.rollback()  # Roll back the session if an exception is raised
            raise  # Raise the exception
        finally:
            session.close()  # Close the session in any case

    def test_connection(self):
        try:
            with self.session_scope() as session:
                session.execute(text("SELECT 1"))  # Wrap in text()
            return True
        except Exception as e:
            print(f"Database connection failed: {str(e)}")
        return False


# At bottom of database.py
_database_manager = DatabaseManager()
assert _database_manager is DatabaseManager(), "Singleton violation detected"