from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
#import connection
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

class Base(DeclarativeBase):
    pass


class ErcotDaPrices(Base):
    __tablename__ = 'ercot_da_prices'
    delivery_date: Mapped[str] = mapped_column(primary_key=True)
    hour_ending: Mapped[str] = mapped_column(primary_key=True)
    repeated_hour_flag: Mapped[str] = mapped_column()
    settlement_point: Mapped[str] = mapped_column(String, primary_key=True)
    settlement_point_price: Mapped[str] = mapped_column()

class ercotDAPrices:
    '''def __init__(self):
        self.session = connection.sessionManager.session'''
    def __init__(self):
        engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\Python Files\Table_Schema\batteryDB.db', echo=False)
        self.Session = sessionmaker(bind=engine)
        #self.session = self.Session()

    def getDAPrices(self, priceDate, settlement_point="HB_HOUSTON"):
        # 1. Convert date_param to string 'YYYY-MM-DD' if it is a date/datetime object
        if isinstance(priceDate, (date, datetime)):
            date_str = priceDate.strftime('%Y-%m-%d')
        else:
            date_str = str(priceDate) # Fallback if already a string
        print(date_str)
        print(settlement_point)
        with self.Session() as session:
            #Generate SQL statement 
            stmt = select(ErcotDaPrices).where(ErcotDaPrices.delivery_date == date_str, ErcotDaPrices.settlement_point == settlement_point).order_by(ErcotDaPrices.hour_ending)
            #Execute SQL statement, this returns a sequence of ErcotDaPrices objects            
            rows = session.scalars(stmt).all()
            print(stmt)
            print(rows[0].delivery_date)
            return [dict(r.__dict__) for r in rows]

    def getAvailableDates(self, settlement_point="HB_HOUSTON"):
        with self.Session() as session:
            #rows = self.Session().query(ErcotDaPrices.delivery_date).filter_by(settlement_point=settlement_point).distinct().order_by(ErcotDaPrices.delivery_date).all()
            rows = select(ErcotDaPrices.delivery_date).where(ErcotDaPrices.settlement_point == settlement_point).distinct().order_by(ErcotDaPrices.delivery_date)
            return [r.delivery_date for r in rows]