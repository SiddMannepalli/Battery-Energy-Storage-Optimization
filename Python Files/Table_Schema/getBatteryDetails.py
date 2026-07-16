from requests import session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from getBatteryHeader import Base

BATTERY_ID = 1

#class Base(DeclarativeBase):
#    pass

class BatteryDetails(Base):
    __tablename__ = 'battery_details'
    battery_id: Mapped[int] = mapped_column(primary_key=True)
    capacity_kwh: Mapped[int] = mapped_column()
    max_charge_kw: Mapped[int] = mapped_column()
    max_discharge_kw: Mapped[int] = mapped_column()
    round_trip_efficiency: Mapped[float] = mapped_column()
    min_soc_pct: Mapped[float] = mapped_column()
    max_soc_pct: Mapped[float] = mapped_column()
    degradation_cost_per_kwh: Mapped[float] = mapped_column()
    soc_initial: Mapped[int] = mapped_column()
    lifecycle: Mapped[int] = mapped_column()
    cycle_limit: Mapped[int] = mapped_column()
    cycle_cost: Mapped[int] = mapped_column()


class batteryDetails:
    '''def __init__(self):
        self.session = connection.sessionManager.session'''
    def __init__(self):
        engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\Python Files\Table_Schema\batteryDB.db', echo=False)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def getBatteryDetails(self, battery_id=BATTERY_ID):
        with self.session as db_session:
            stmt = select(BatteryDetails).where(BatteryDetails.battery_id == battery_id)
            battery = self.session.scalars(stmt).all()
            return battery


