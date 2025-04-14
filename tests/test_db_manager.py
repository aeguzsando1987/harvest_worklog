import sys  
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.database import DatabaseManager

def test_connection_and_migration():
    print("DATABASE CONNECTION & MIGRATION TEST")

    try:
        db = DatabaseManager()
        db.initialize()

        print("\n1. Testing database connection...")
        connection_status = db.test_connection()
        print(f"Conection status: {'Success' if connection_status else 'Failed'}")

        print("\n2. Creating tables...")
        db.Base.metadata.create_all(db.engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"[ERROR] Operation failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection_and_migration()






