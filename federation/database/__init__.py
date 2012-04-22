# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''This submodule acts as an interface between an SQL database for
persistent storage and an object oriented form that the game itself
likes to use.
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

LOCATION = 'sqlite:///:memory:'
Base = declarative_base()

def make_db(location):
    '''This provides the code that sets up SQLAlchemy so that it can
    talk to the database. It returns a session instance.
    '''
    engine = create_engine(location, echo=False)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return session()

import federation.database.database, federation.database.model

session = make_db(LOCATION)
