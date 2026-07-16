import pandas as pd
from sqlalchemy import create_engine

#engine = create_engine('sqlite:///C:\\Sidd\\Battery Optimization Project\\batteryDB.db', echo=False)
engine = create_engine('sqlite:///batteryDB.db', echo=False)
csv_file_path = 'C:\\Sidd\\Battery Optimization Project\\CSV Data Files\\BatteryDetailsCSV.csv'

df = pd.read_csv(csv_file_path)

df.to_sql(name='battery_details', con=engine, if_exists='replace', index=False)

print("Data successfully loaded into the database!")
