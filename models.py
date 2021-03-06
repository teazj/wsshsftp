# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Sequence, Unicode, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from ConfigParser import ConfigParser

my_config = ConfigParser()
my_config.read('config.ini')

Base = declarative_base()

address = my_config.get('database', 'address')
mysql_engine = create_engine(address)


def create_db_session():
    return scoped_session(sessionmaker(bind=mysql_engine, autoflush=True, autocommit=False))


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(BigInteger, Sequence('user_id_seq'), primary_key=True)
    email = Column(Unicode(64), nullable=False, unique=True)
    password = Column(Unicode(64), nullable=False)
    last_login_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)


class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    id = Column(BigInteger, Sequence('server_id_seq'), primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    server_name = Column(Unicode(64), nullable=True, default='My Server')
    host = Column(Unicode(64), nullable=False)
    port = Column(Integer, nullable=False, default=22)
    username = Column(Unicode(64), nullable=False)
    password = Column(Unicode(64), nullable=True)
    last_login_time = Column(DateTime, nullable=True, default=None)

if __name__ == '__main__':
    Base.metadata.create_all(mysql_engine)
