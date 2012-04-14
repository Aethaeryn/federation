#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

# LOCATION = 'sqlite:////tmp/foo.sqlite'
LOCATION = 'sqlite:///:memory:'
Base     = declarative_base()

class Database():
    def __init__(self, location):
        self.engine = create_engine(location, echo=False)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

class Game(Base):
    __tablename__ = 'game'

    id            = Column(Integer, primary_key=True)
    server_name   = Column(String(80), unique=True)
    turn          = Column(Integer)
    start_year    = Column(Integer)
    turns_per_day = Column(Integer)

    def __init__(self, server_name, start_year, turns_per_day):
        self.server_name   = server_name
        self.start_year    = start_year
        self.turns_per_day = turns_per_day
        self.turn          = 0

    def get_date(self):
        """ Converts the turn number into a calendar date. Each month is
        represented by an index on the list 'months'. An Earth calendar is
        used such that every 12 turns is a year, and each year has 12 months.
        """

        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']

        month = self.turn % 12
        year  = self.turn / 12
        year += self.start_year

        return months[month], year

    def __repr__(self):
        return '<Game %s (%s)>' % (self.server_name, self.id)

class Component(Base):
    __tablename__ = 'component'

    id         = Column(Integer, primary_key=True)
    name       = Column(String(80))
    enabled    = Column(Boolean)
    hurt       = Column(Integer)

    ship_id    = Column(Integer, ForeignKey('spacecraft.id'))
    spacecraft = relationship('Spacecraft', backref=backref('components', order_by=id))

    def __init__(self, name, spacecraft):
        self.name       = name
        self.spacecraft = spacecraft
        self.enabled    = True
        self.hurt       = 0

    def __repr__(self):
        return '<Component %s>' % (self.name)

class Spacecraft(Base):
    __tablename__ = 'spacecraft'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80))
    custom_name = Column(String(80))

    owner_id    = Column(Integer, ForeignKey('player.id'))
    fleet_id    = Column(Integer, ForeignKey('fleet.id'))
    map_id      = Column(Integer, ForeignKey('map.id'))
    owner       = relationship('Player', backref=backref('spacecraft', order_by=id))
    fleet       = relationship('Fleet', backref=backref('spacecraft', order_by=id))
    location    = relationship('Map', backref=backref('spacecraft', order_by=id))

    x_position  = Column(Integer)
    y_position  = Column(Integer)

    def __init__(self, name, custom_name, owner):
        self.name        = name
        self.custom_name = custom_name
        self.owner       = owner

    def __repr__(self):
        return '<Spacecraft %s (%s)>' % (self.custom_name, self.name)

class Federation(Base):
    __tablename__ = 'federation'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80), unique=True)
    date        = Column(DateTime)
    cash        = Column(Integer)
    tax_rate    = Column(Integer)
    shared_view = Column(Boolean)

    def __init__(self, name, founder):
        self.name    = name
        self.founder = founder
        self.date    = datetime.utcnow()

    def __repr__(self):
        return '<Federation %s>' % (self.name)

class Player(Base):
    __tablename__ = 'player'

    id         = Column(Integer, primary_key=True)
    username   = Column(String(80), unique=True)
    game_name  = Column(String(80))
    email      = Column(String(80))
    date       = Column(DateTime)
    cash       = Column(Integer)
    income     = Column(Integer)
    research   = Column(Integer)

    federation = relationship('Federation', backref=backref('players', order_by = id))
    fed_id     = Column(Integer, ForeignKey('federation.id'))
    fed_found  = Column(Boolean)
    fed_leader = Column(Boolean)
    fed_rank   = Column(Integer)
    fed_role   = Column(String(80))

    def __init__(self, username, game_name, email):
        self.username   = username
        self.game_name  = game_name
        self.email      = email
        self.date       = datetime.utcnow()
        self.cash       = 0
        self.income     = 0
        self.research   = 0

    def get_player_info(self):
        """ Returns the information that the UI expects.
        """

        stats               = {}
        stats['name']       = self.game_name
        stats['federation'] = self.federation.name
        stats['cash']       = self.cash
        stats['income']     = self.income
        stats['research']   = self.research
        stats['ships']      = len(self.spacecraft)
        stats['fleets']     = len(self.fleets)
        stats['territory']  = len(self.territory)

        return stats

    def __repr__(self):
        return '<Player %s (%s)>' % (self.game_name, self.username)

class Fleet(Base):
    __tablename__ = 'fleet'

    id         = Column(Integer, primary_key=True)
    name       = Column(String(80))

    fed_id     = Column(Integer, ForeignKey('federation.id'))
    cmd_id     = Column(Integer, ForeignKey('player.id'))
    dep_id     = Column(Integer, ForeignKey('player.id'))
    federation = relationship('Federation', backref=backref('fleets', order_by=id))
    commander  = relationship('Player', backref=backref('fleets', order_by=id),
                              primaryjoin='Player.id==Fleet.cmd_id')
    deputy     = relationship('Player', backref=backref('fleets_d', order_by=id),
                              primaryjoin='Player.id==Fleet.dep_id')

    def __init__(self, name, commander):
        self.name = name
        self.commander = commander

    def __repr__(self):
        return '<Fleet %s %s (%s)>' % (self.id, self.name, self.commander)

class Unit(Base):
    __tablename__ = 'unit'

    id   = Column(Integer, primary_key=True)
    name = Column(String(80))
    hurt = Column(Integer)

    def __init__(self, name):
        self.name = name
        self.hurt = 0

    def __repr__(self):
        return '<Unit %s %s>' % (self.name, self.id)

class Body(Base):
    __tablename__ = 'body'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80))
    custom_name = Column(String(80))
    variant     = Column(String(80))

    owner_id    = Column(Integer, ForeignKey('player.id'))
    map_id      = Column(Integer, ForeignKey('map.id'))
    owner       = relationship('Player', backref=backref('territory', order_by=id))
    location    = relationship('Map', backref=backref('bodies', order_by=id))

    x_position  = Column(Integer)
    y_position  = Column(Integer)

    def __init__(self, name, custom_name, variant):
        self.name        = name
        self.custom_name = custom_name
        self.variant     = variant

    def __repr__(self):
        return '<Body %s (%s %s)>' % (self.custom_name, self.name, self.id)

class Structure(Base):
    __tablename__ = 'structure'

    id      = Column(Integer, primary_key=True)
    name    = Column(String(80))
    hurt    = Column(Integer)
    body_id = Column(Integer, ForeignKey('body.id'))
    body    = relationship('Body', backref=backref('structures', order_by=id))

    def __init__(self, name, body):
        self.name = name
        self.body = body
        self.hurt = 0

    def __repr__(self):
        return '<Structure %s %s (%s %s)>' % (self.name, self.id, self.body.custom_name, self.body.id)

class Map(Base):
    __tablename__ = 'map'

    id         = Column(Integer, primary_key=True)
    map_type   = Column(String(80))
    name       = Column(String(80))
    x_size     = Column(Integer)
    y_size     = Column(Integer)
    x_position = Column(Integer)
    y_position = Column(Integer)

    def __init__(self, name, x_size, y_size, x_pos, y_pos, map_type):
        self.name       = name
        self.x_size     = x_size
        self.y_size     = y_size
        self.x_position = x_position
        self.y_position = y_position
        self.map_type   = map_type

    def __repr__(self):
        return '<%s %s (%s x %s)>' % (self.map_type, self.name, self.x_size, self.y_size)

db      = Database(LOCATION)
session = db.session

def debug():
    # game = database.Game('Test', 2500, 1)

    # Player
    player = Player('michael', 'Mike', 'michael@example.com')
    player.cash = 20
    player.income = 2
    player.research = 4

    federation = Federation('Empire', 1)
    player.federation = federation

    session.add(player)

    # Spacecraft
    spaceships = ['Battle Frigate', 'Battle Frigate', 'Basic Fighter', 'Cruiser']

    for spaceship in spaceships:
        db_spaceship = Spacecraft(spaceship, 'Foobar', player)
        session.add(db_spaceship)

    spaceship_foo = Spacecraft('Carrier', 'Barfoo', player)

    # Fleet
    session.add(Fleet('Zombie Raptor', player))

    # Federation
    session.add(federation)

    # Component
    session.add(Component('Small Hull', spaceship_foo))

    # This must come last!
    session.commit()
