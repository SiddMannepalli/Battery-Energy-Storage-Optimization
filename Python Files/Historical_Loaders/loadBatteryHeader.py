import os
import sys
import pandas as pd
from sqlalchemy import inspect, text

#Make the shared database connection in Table_Schema/db.py importable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Table_Schema'))
from db import engine, PROJECT_DIR

csv_file_path = os.path.join(PROJECT_DIR, 'CSV Data Files', 'BatteryHeaderCSV.csv')
df = pd.read_csv(csv_file_path)

#Clear out the old rows and append the new ones, rather than dropping the table
#(dropping would remove its keys and fails in PostgreSQL when another table references it)
with engine.begin() as conn:
    if inspect(conn).has_table('battery_header'):
        conn.execute(text('DELETE FROM battery_header'))
    df.to_sql(name='battery_header', con=conn, if_exists='append', index=False)

print("Data successfully loaded into the database!")
