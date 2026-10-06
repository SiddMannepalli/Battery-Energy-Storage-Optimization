import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Folder this file lives in, and the top-level project folder (two levels up)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

#Read settings from <project>/.env if it exists (e.g. DATABASE_URL=postgresql+psycopg://...)
load_dotenv(os.path.join(PROJECT_DIR, '.env'))

#Default to the local SQLite file if DATABASE_URL is not set
SQLITE_PATH = os.path.join(SCRIPT_DIR, 'batteryDB.db')
DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{SQLITE_PATH}')

#One engine and session factory shared by every file in the project
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
