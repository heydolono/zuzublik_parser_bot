import os
from dotenv import load_dotenv
from sqlalchemy import (create_engine, Column, Integer, String, Float,
                        ForeignKey, DateTime, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    xpath = Column(String, nullable=False)
    average_price = Column(Float, nullable=True)
    prices = relationship("Price", back_populates="site")

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    site = relationship("Site", back_populates="prices")


def init_db():
    Base.metadata.create_all(bind=engine)