import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url, text
from sqlalchemy.orm import sessionmaker

#Folder this file lives in, and the top-level project folder (two levels up)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

#Read settings from <project>/.env if it exists (e.g. DATABASE_URL=postgresql+psycopg://...)
load_dotenv(os.path.join(PROJECT_DIR, '.env'))

#Default to the local SQLite file if DATABASE_URL is not set
SQLITE_PATH = os.path.join(SCRIPT_DIR, 'batteryDB.db')
DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{SQLITE_PATH}')


def createDatabaseIfMissing(database_url):
    #SQLite creates its database file automatically on first connect; PostgreSQL does not,
    #so connect to the server's built-in 'postgres' database and create ours if it isn't there yet
    url = make_url(database_url)
    if url.get_backend_name() != 'postgresql':
        return
    server = create_engine(url.set(database='postgres'), isolation_level='AUTOCOMMIT')
    with server.connect() as conn:
        exists = conn.scalar(text('SELECT 1 FROM pg_database WHERE datname = :name'), {'name': url.database})
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{url.database}"'))
            print(f"Created PostgreSQL database '{url.database}'")
    server.dispose()


createDatabaseIfMissing(DATABASE_URL)

#One engine and session factory shared by every file in the project
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
