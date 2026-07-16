from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from createBatteryHeaderTable import Base
from sqlalchemy.schema import CreateTable


engine = create_engine('sqlite:///batteryDB.db', echo=True)

#class Base(DeclarativeBase):
#    pass

class Battery_Details(Base):
    __tablename__ = 'battery_details'
    detail_id: Mapped[int] = mapped_column(primary_key=True)
    battery_id: Mapped[int] = mapped_column(ForeignKey("battery_header.battery_id"))
    capacity_kwh: Mapped[float] = mapped_column()
    max_charge_kw: Mapped[float] = mapped_column()
    max_discharge_kw: Mapped[float] = mapped_column()
    round_trip_efficiency: Mapped[float] = mapped_column()
    min_soc_pct: Mapped[float] = mapped_column()
    max_soc_pct: Mapped[float] = mapped_column()
    degradation_cost_per_kwh: Mapped[float] = mapped_column()
    soc_initial: Mapped[float] = mapped_column()
    lifecycle: Mapped[float] = mapped_column()
    cycle_limit: Mapped[float] = mapped_column()
    cycle_cost: Mapped[float] = mapped_column()

#print(CreateTable(Battery_Details.__table__).compile(engine))

Base.metadata.create_all(engine)
print("Database tables created successfully!")

'''
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
'''