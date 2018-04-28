#!/usr/bin/env python
# encoding: utf-8
# author: Lock
# time: 2018/4/28 11:36

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

CONFIG = {
    'db_host': '127.0.0.1',
    'db_user': 'root',
    'db_pass': '',
    'db_port': 3306,
    'db_name': 'crawl'
}

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' % (
    CONFIG.get('db_user'),
    CONFIG.get('db_pass'),
    CONFIG.get('db_host'),
    CONFIG.get('db_port'),
    CONFIG.get('db_name'),
))

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
