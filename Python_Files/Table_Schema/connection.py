from db import engine, Session

class sessionManager:
<<<<<<< HEAD:Python_Files/Table_Schema/connection.py
    #engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\batteryDB.db', echo=False)
    engine = create_engine(r'sqlite:////Users/siddm/Library/CloudStorage/OneDrive-Personal/Battery-Energy-Storage-Optimization/Python_Files/Table_Schema/batteryDB.db', echo=False)
    Session = sessionmaker(bind=engine)
=======
    engine = engine
    Session = Session
>>>>>>> 4e5f386d1a596fadb7e2ef62a80fa5ee0db5a66e:Python Files/Table_Schema/connection.py
    session = Session()