from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from createBatteryHeaderTable import Base

SQLITE_URL = "sqlite:////Users/siddm/Library/CloudStorage/OneDrive-Personal/Battery-Energy-Storage-Optimization/Python Files/Table_Schema/batteryDB.db"
POSTGRES_URL = "postgresql+psycopg2://postgres:password@localhost:5432/batteryDB"

sqlite_engine = create_engine(SQLITE_URL)
postgres_engine = create_engine(POSTGRES_URL)

def migrate_database():

    # 2. Automatically create the schema tables in PostgreSQL
    Base.metadata.create_all(postgres_engine)

    # 3. Create a session for the target PostgreSQL DB
    PgSession = sessionmaker(bind=postgres_engine)
    pg_session = PgSession()

    # 4. Migrate data table by table in the correct dependency order
    # sorted_tables ensures parent tables migrate before child tables
    with sqlite_engine.connect() as sqlite_conn:
        for table in Base.metadata.sorted_tables:
            
            # Fetch all rows from the SQLite table
            result = sqlite_conn.execute(select(table))
            
            # Convert rows to mappings (dictionaries)
            rows = [row._mapping for row in result]

            sqlite_conn.execute(table.insert(), rows)
            
    with postgres_engine.connect() as pg_conn:
        for table in Base.metadata.sorted_tables:
            # Look for an integer primary key column named 'id'
            if 'id' in table.columns and table.columns['id'].primary_key:
                seq_query = f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), COALESCE(max(id), 1)) FROM {table.name};"
                try:
                    pg_conn.execute(text(seq_query))
                except Exception:
                    # Ignore if the table does not use a standard Postgres serial sequence
                    pass


if __name__ == "__main__":
    from sqlalchemy import text
    migrate_database()
