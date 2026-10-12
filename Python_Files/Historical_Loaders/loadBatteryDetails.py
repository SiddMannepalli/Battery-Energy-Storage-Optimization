import os
import sys
import pandas as pd
from sqlalchemy import inspect, text

<<<<<<< HEAD:Python_Files/Historical_Loaders/loadBatteryDetails.py

#engine = create_engine('sqlite:///C:\\Sidd\\Battery Optimization Project\\batteryDB.db', echo=False)
engine = create_engine('sqlite:///batteryDB.db', echo=False)
#Old file path on old windows laptop
#csv_file_path = 'C:\\Sidd\\Battery Optimization Project\\CSV Data Files\\BatteryDetailsCSV.csv'
#New file path on Macbook
csv_file_path = '/Users/siddm/Library/CloudStorage/OneDrive-Personal/Battery-Energy-Storage-Optimization/CSV Data Files/BatteryDetailsCSV.csv'
=======
#Make the shared database connection in Table_Schema/db.py importable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Table_Schema'))
from db import engine, PROJECT_DIR

csv_file_path = os.path.join(PROJECT_DIR, 'CSV Data Files', 'BatteryDetailsCSV.csv')
>>>>>>> 4e5f386d1a596fadb7e2ef62a80fa5ee0db5a66e:Python Files/Historical_Loaders/loadBatteryDetails.py
df = pd.read_csv(csv_file_path)

#Clear out the old rows and append the new ones, rather than dropping the table
#(dropping would remove its keys and fails in PostgreSQL when another table references it)
with engine.begin() as conn:
    if inspect(conn).has_table('battery_details'):
        conn.execute(text('DELETE FROM battery_details'))
    df.to_sql(name='battery_details', con=conn, if_exists='append', index=False)

print("Data successfully loaded into the database!")
