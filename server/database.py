#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from server import app, data
from sqlalchemy import create_engine, Column, Integer, Boolean, String
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#### TODO: Put in an actual location and turn off echo
engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)

class Alliance(Base):
    __tablename__ = 'alliance'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80), unique=True)
    founder     = Column(String(80))
    date        = Column(DateTime())
    cash        = Column(Integer)
    tax_rate    = Column(Integer)
    shared_view = Column(Boolean)
    #### store leaders/ranks/roles/etc.

    def __init__(self, name, founder):
        self.name    = name
        self.founder = founder
        self.date    = data.Time.get()

    def __repr__(self):
        return '<Alliance %s>' % (self.name)

class Player(Base):
    __tablename__ = 'player'

    id         = Column(Integer, primary_key=True)
    username   = Column(String(80), unique=True)
    game_name  = Column(String(80))
    email      = Column(String(80))
    date       = Column(DateTime())
    cash       = Column(Integer)
    income     = Column(Integer)
    research   = Column(Integer)
    federation = Column(String(80))
    #### count fleets, territories, ships
    #### associate ownership with player
    #### associate with membership in the actual alliance

    def __init__(self, username, game_name, email):
        self.username  = username
        self.game_name = game_name
        self.email     = email
        self.date      = date.Time.get()

    def __repr__(self):
        return '<Player %s (%s)>' % (self.game_name, self.username)

class Fleet(Base):
    __tablename__ = 'fleet'

    #### hold ships
    #### hold players
    #### count ships/players

    id         = Column(Integer, primary_key=True)
    name       = Column(String(80))
    federation = Column(String(80))
    commander  = Column(String(80))
    deputy     = Column(String(80))

    def __init__(self, name, commander):
        self.name = name
        self.commander = commander

    def __repr__(self):
        return '<Fleet %s %s (%s)>' % (self.id, self.name, self.commander)

Base.metadata.create_all(engine)

foo = Alliance("me", "you")
session = Session()
session.add(foo)
session.commit()
