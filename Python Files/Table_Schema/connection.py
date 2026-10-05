from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class sessionManager:
    #engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\batteryDB.db', echo=False)
    engine = create_engine(r'sqlite:////Users/siddm/Library/CloudStorage/OneDrive-Personal/Battery-Energy-Storage-Optimization/Python Files/Table_Schema/batteryDB.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()