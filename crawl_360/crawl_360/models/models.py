# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Butian(Base):
    __tablename__ = 'butian'

    id = Column(Integer, primary_key=True)
    author = Column(String(100), nullable=False, server_default=text("''"))
    company_name = Column(String(100), nullable=False, server_default=text("''"))
    vul_level = Column(String(100), nullable=False, server_default=text("''"))
    vul_name = Column(String(100), nullable=False, server_default=text("''"))
    vul_money = Column(Numeric(10, 2), nullable=False)
    vul_find_time = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    link_url = Column(String(255), nullable=False, server_default=text("''"))
    create_time = Column(DateTime, nullable=False)
