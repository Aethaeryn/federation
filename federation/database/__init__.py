# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''This submodule acts as an interface between an SQL database for
persistent storage and an object oriented form that the game itself
likes to use.
'''
from sqlalchemy.ext.declarative import declarative_base

Base      = declarative_base()
