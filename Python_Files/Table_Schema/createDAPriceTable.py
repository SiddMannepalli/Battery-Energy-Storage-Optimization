import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from createBatteryHeaderTable import Base


engine = create_engine('sqlite:///batteryDB.db', echo=False)

#class Base(DeclarativeBase):
#    pass


class Ercot_DA_Prices(Base):
    __tablename__ = 'ercot_da_prices'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    delivery_date: Mapped[datetime] = mapped_column()
    hour_ending: Mapped[int] = mapped_column()
    repeated_hour_flag: Mapped[bool] = mapped_column()
    settlement_point: Mapped[str] = mapped_column(String)
    settlement_point_price: Mapped[float] = mapped_column()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

