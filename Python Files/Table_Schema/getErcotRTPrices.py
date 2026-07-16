from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, select   
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass


class ErcotRTPrices(Base):
    __tablename__ = 'ercot_rt_prices'
    delivery_date: Mapped[str] = mapped_column(primary_key=True)
    delivery_hour: Mapped[int] = mapped_column(primary_key=True)
    delivery_interval: Mapped[int] = mapped_column()
    settlement_point_name: Mapped[str] = mapped_column(String, primary_key=True)
    settlement_point_type: Mapped[str] = mapped_column(String, primary_key=True)
    settlement_point_price: Mapped[float] = mapped_column()

class ercotRTPrices:
    '''def __init__(self):
        self.session = connection.sessionManager.session'''
    def __init__(self):
        engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\Python Files\Table_Schema\batteryDB.db', echo=False)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
    def getRTPrices(self, date, settlement_point="HB_HOUSTON"):
        #with self.Session() as session:
            #rows = self.Session().query(ErcotRTPrices).filter_by(delivery_date=date, settlement_point=settlement_point).order_by(ErcotRTPrices.hour_ending).all()
            rows = select(ErcotRTPrices).where(ErcotRTPrices.delivery_date == date, ErcotRTPrices.settlement_point == settlement_point).order_by(ErcotRTPrices.hour_ending)
            return [dict(r.__dict__) for r in rows]

    def getAvailableDates(self, settlement_point="HB_HOUSTON"):
        #with self.Session() as session:
            #rows = self.Session().query(ErcotRTPrices.delivery_date).filter_by(settlement_point=settlement_point).distinct().order_by(ErcotRTPrices.delivery_date).all()
            rows = select(ErcotRTPrices.delivery_date).where(ErcotRTPrices.settlement_point == settlement_point).distinct().order_by(ErcotRTPrices.delivery_date)
            return [r.delivery_date for r in rows]