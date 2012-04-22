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

class Database():
    '''Acts as a connection layer between a SQL database session and
    the rest of the SQLAlchemy-using code.
    '''
    def __init__(self, location):
        self.engine = create_engine(location, echo=False)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

import federation.database.database, federation.database.model

db      = Database(LOCATION)
session = db.session
