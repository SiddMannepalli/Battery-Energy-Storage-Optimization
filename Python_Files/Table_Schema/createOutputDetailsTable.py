from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from createOutputHeaderTable import Base

engine = create_engine('sqlite:///batteryDB.db', echo=False)

class Ercot_RT_Prices(Base):
    __tablename__ = 'output_details'
    id: Mapped[int] = mapped_column(primary_key=True)
    output_id: Mapped[int] = mapped_column(ForeignKey('output_header.output_id'))
    hour: Mapped[int] = mapped_column()
    action: Mapped[str] = mapped_column()
    charge_kw: Mapped[float] = mapped_column()
    discharge_kw: Mapped[float] = mapped_column()
    soc_kw: Mapped[float] = mapped_column()
    price_mwh: Mapped[float] = mapped_column()
    revenue: Mapped[float] = mapped_column()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
