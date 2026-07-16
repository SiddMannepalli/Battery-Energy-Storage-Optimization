from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from createBatteryHeaderTable import Base, Battery_Header


#engine = create_engine('sqlite:///C:\\Sidd\\Battery Optimization Project\\batteryDB.db', echo=True)
engine = create_engine('sqlite:///batteryDB.db', echo=True)

#class Base(DeclarativeBase):
#    pass

class outputHeader(Base):
    __tablename__ = 'output_header'
    output_id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[int] = mapped_column()
    battery_id: Mapped[int] = mapped_column(ForeignKey('battery_header.battery_id'))
    #date: Mapped[datetime] = mapped_column()
    date: Mapped[str] = mapped_column()
    optimization_type: Mapped[str] = mapped_column()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
