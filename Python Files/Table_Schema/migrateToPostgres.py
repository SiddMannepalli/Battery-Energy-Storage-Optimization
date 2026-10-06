#Copies every table from the SQLite file (batteryDB.db) into the PostgreSQL database in DATABASE_URL.
#Run once, after creating an empty PostgreSQL database and setting DATABASE_URL in <project>/.env:
#    python migrateToPostgres.py
from sqlalchemy import (create_engine, MetaData, Table, Column, Index, ForeignKey, select, func, text,
                        BigInteger, Integer, Float, Text, String)
from db import engine as pg_engine, SQLITE_PATH

#PostgreSQL table definitions. Columns match the existing SQLite tables, with primary keys added
#where the SQLite tables had none (PostgreSQL needs them for the foreign keys to work)
metadata = MetaData()

battery_header = Table('battery_header', metadata,
    Column('battery_id', BigInteger, primary_key=True, autoincrement=False),
    Column('name', Text),
    Column('location', Text),
    Column('owner', Text),
    Column('iso', Text),
)

battery_details = Table('battery_details', metadata,
    Column('battery_id', BigInteger, ForeignKey('battery_header.battery_id'), primary_key=True, autoincrement=False),
    Column('capacity_kwh', BigInteger),
    Column('max_charge_kw', BigInteger),
    Column('max_discharge_kw', BigInteger),
    Column('round_trip_efficiency', Float),
    Column('min_soc_pct', Float),
    Column('max_soc_pct', Float),
    Column('degradation_cost_per_kwh', Float),
    Column('soc_initial', BigInteger),
    Column('lifecycle', BigInteger),
    Column('cycle_limit', BigInteger),
    Column('cycle_cost', BigInteger),
)

ercot_da_prices = Table('ercot_da_prices', metadata,
    Column('delivery_date', Text),
    Column('hour_ending', Text),
    Column('repeated_hour_flag', Text),
    Column('settlement_point', Text),
    Column('settlement_point_price', Text),
    Index('ix_ercot_da_prices_point_date', 'settlement_point', 'delivery_date'),
)

ercot_rt_prices = Table('ercot_rt_prices', metadata,
    Column('delivery_date', Text),
    Column('delivery_hour', BigInteger),
    Column('delivery_interval', BigInteger),
    Column('repeated_hour_flag', Text),
    Column('settlement_point_name', Text),
    Column('settlement_point_type', Text),
    Column('settlement_point_price', Text),
    Index('ix_ercot_rt_prices_point_date', 'settlement_point_name', 'delivery_date'),
)

output_header = Table('output_header', metadata,
    Column('output_id', Integer, primary_key=True),
    Column('version', Integer, nullable=False),
    Column('battery_id', BigInteger, ForeignKey('battery_header.battery_id'), nullable=False),
    Column('date', String, nullable=False),
    Column('optimization_type', String, nullable=False),
)

output_details = Table('output_details', metadata,
    Column('id', Integer, primary_key=True),
    Column('output_id', Integer, ForeignKey('output_header.output_id'), nullable=False),
    Column('hour', Integer, nullable=False),
    Column('action', String, nullable=False),
    Column('charge_kw', Float, nullable=False),
    Column('discharge_kw', Float, nullable=False),
    Column('soc_kw', Float, nullable=False),
    Column('price_mwh', Float, nullable=False),
    Column('revenue', Float, nullable=False),
)

#Auto-numbered id columns whose counters must be moved past the copied ids
SERIAL_COLUMNS = [('output_header', 'output_id'), ('output_details', 'id')]
BATCH_SIZE = 10000


def convert(table, row):
    #SQLite lets any value go in any column (e.g. output_header.date holds both '3/12/2026' and 0);
    #PostgreSQL does not, so turn values headed for text columns into strings
    row = dict(row)
    for col in table.columns:
        value = row.get(col.name)
        if value is not None and isinstance(col.type, (Text, String)) and not isinstance(value, str):
            row[col.name] = str(value)
    return row


def main():
    if pg_engine.dialect.name != 'postgresql':
        raise SystemExit(f'DATABASE_URL must point to PostgreSQL (it is currently {pg_engine.url}). Set it in <project>/.env')

    sqlite_engine = create_engine(f'sqlite:///{SQLITE_PATH}')

    metadata.create_all(pg_engine)

    with pg_engine.begin() as pg:
        for table in metadata.sorted_tables:
            if pg.scalar(select(func.count()).select_from(table)):
                raise SystemExit(f'Table {table.name} in PostgreSQL already has data; empty it first so nothing is copied twice.')

        #Parent tables first (sorted_tables follows the foreign keys) so every reference already exists
        for table in metadata.sorted_tables:
            copied = 0
            with sqlite_engine.connect() as lite:
                #Plain SQL returns the values exactly as stored, without SQLAlchemy trying to parse them
                result = lite.execute(text(f'SELECT * FROM {table.name}')).mappings()
                while batch := result.fetchmany(BATCH_SIZE):
                    pg.execute(table.insert(), [convert(table, row) for row in batch])
                    copied += len(batch)
            print(f'{table.name}: copied {copied} rows')

        for table_name, column in SERIAL_COLUMNS:
            pg.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table_name}', '{column}'), "
                f"COALESCE((SELECT MAX({column}) FROM {table_name}), 0) + 1, false)"
            ))

    print('Migration complete!')


if __name__ == '__main__':
    main()
