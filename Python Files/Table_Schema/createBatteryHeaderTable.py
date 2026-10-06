import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


from db import engine

class Base(DeclarativeBase):
    pass

class Battery_Header(Base):
    __tablename__ = 'battery_header'

    battery_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    owner: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column()
    iso: Mapped[str] = mapped_column(String)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
