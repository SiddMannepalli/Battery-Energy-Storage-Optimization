import sys
sys.path.append(r'C:\Sidd\Battery Optimization Project\Python Files\Table_Schema')

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from createOutputHeaderTable import outputHeader as output_header
from createOutputDetailsTable import Ercot_RT_Prices as output_details


class outputProcessor():
    def __init__(self):
        engine = create_engine(r'sqlite:///C:\Sidd\Battery Optimization Project\Python Files\Table_Schema\batteryDB.db', echo=False)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def getMaxVersion(self, battery_id, date):
        stmt = select(func.max(output_header.version)).where(
            output_header.battery_id == battery_id,
            output_header.date == date
        )
        maxVersion = self.session.scalar(stmt)
        #return maxVersion
        return maxVersion if maxVersion is not None else 0

    def getMaxOutputID(self):
        stmt = select(func.max(output_header.output_id))
        maxOutputID = self.session.scalar(stmt)
        return maxOutputID

    def saveOutputHeader(self, battery_id, date, optimization_type):
        version = self.getMaxVersion(battery_id, date) + 1
        new_header = output_header(
            version=version,
            battery_id=battery_id,
            date=date,
            optimization_type=optimization_type
        )
        self.session.add(new_header)
        self.session.commit()
        self.session.refresh(new_header)
        return new_header.output_id

    def saveOutputDetails(self, output_id, schedule):
        for row in schedule:
            detail = output_details(
                output_id=output_id,
                hour=row['hour'],
                action=row['action'],
                charge_kw=row['charge_kw'],
                discharge_kw=row['discharge_kw'],
                soc_kw=row['soc_kw'],
                price_mwh=row['price_mwh'],
                revenue=row['revenue']
            )
            self.session.add(detail)
        self.session.commit()

    def getOptData(self):
        stmt = (
            select(output_header, output_details)
            .join(output_details, output_header.output_id == output_details.output_id)
        )
        return self.session.execute(stmt).all()
    
    '''def getOptData(self, ):
        stmt = (
            select(output_header, output_details)
            .join(output_details, output_header.output_id == output_details.output_id)
        )
        return self.session.execute(stmt).all()
    '''
    def getOptDataBatteryID(self, battery_id):
        stmt = (
            select(output_header, output_details)
            .join(output_details, output_header.output_id == output_details.output_id)
            .where(output_header.battery_id == battery_id)
        )
        return self.session.execute(stmt).all()
    
    def getOptDataDate(self, date):
        stmt = (
            select(output_header, output_details)
            .join(output_details, output_header.output_id == output_details.output_id)
            .where(output_header.date == date)
        )
        return self.session.execute(stmt).all()
