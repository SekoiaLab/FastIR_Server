from .db import DB
from sqlalchemy import String, Integer, Column, DateTime, Boolean


class Ping(DB.Model):
    __tablename__ = 'ping'
    id = Column(Integer, primary_key=True)
    hostname = Column(String, unique=True, index=True)
    date = Column(DateTime)


class Order(DB.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    hostname = Column(String, unique=True, index=True)
    config_filename = Column(String)
    active = Column(Boolean, default=False)
