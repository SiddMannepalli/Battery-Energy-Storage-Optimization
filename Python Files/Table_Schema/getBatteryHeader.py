from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass

class BatteryHeader(Base):
    __tablename__ = 'battery_header'
    battery_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    owner: Mapped[str] = mapped_column(String)
    iso: Mapped[str] = mapped_column(String)

class batteryHeader:
    '''def __init__(self):
        self.session = connection.sessionManager.session'''
    def __init__(self):
        engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\Python Files\Table_Schema\batteryDB.db', echo=False)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
    def getBatteryHeader(self, battery_id=1):
        '''with self.session as session:
            #batteryHeader = session.query(BatteryHeader).filter_by(battery_id=battery_id).one()
            batteryHeader = select(BatteryHeader).where(BatteryHeader.battery_id == battery_id)
            return batteryHeader
        '''
        with self.session as session:
            #Generate SQL statement 
            stmt = select(BatteryHeader).where(BatteryHeader.battery_id == battery_id)
            #Execute SQL statement, this returns a sequence of BatteryHeader objects
            battery = self.session.scalars(stmt).all()
            #Returing a sequence of BatteryHeader Objects
            return battery

    def getNumberOfBatteries(self):
        with self.session as session:
            count = session.query(BatteryHeader).count()
            return count
        
    def getBatteryLocations(self):
        with self.session as session:
            locations = session.query(BatteryHeader.location).distinct().all()
            return [loc[0] for loc in locations]