from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class sessionManager:
    engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\batteryDB.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()