'''Uses SQLAlchemy to store data a SQL database.
'''
from datetime import datetime
from federation.database import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

class Component(Base):
    '''Stores *all* of the components that are in existence in the
    game and points them at the spacecraft they are installed in.

    Only the information that will differ between components in action
    are stored here. The rest of the stats are stored in
    ModelComponent because they do not regularly change.
    '''
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
    '''Stores *all* of the spacecraft in the game! This also points to
    their relationships to their owner, their fleet, their location,
    and their components.
    '''
    __tablename__ = 'spacecraft'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80))
    custom_name = Column(String(80))
    owner_id    = Column(Integer, ForeignKey('player.id'))
    x_position  = Column(Integer)
    y_position  = Column(Integer)

    def __init__(self, name, custom_name, owner):
        self.name        = name
        self.custom_name = custom_name
        self.owner       = owner

    def __repr__(self):
        return '<Spacecraft %s (%s)>' % (self.custom_name, self.name)

class Player(Base):
    '''Stores information about every user in the game.
    '''
    __tablename__ = 'player'

    id         = Column(Integer, primary_key=True)
    username   = Column(String(80), unique=True)
    cash       = Column(Integer)
    date       = Column(DateTime)
    email      = Column(String(80))
    game_name  = Column(String(80))

    def __init__(self, username, game_name, email):
        self.username   = username
        self.game_name  = game_name
        self.email      = email
        self.date       = datetime.utcnow()
        self.cash       = 0
        self.income     = 0

    def get_player_info(self):
        '''Returns the information that the UI expects.
        '''
        stats               = {}
        stats['name']       = self.game_name
        stats['federation'] = self.federation.name
        stats['cash']       = self.cash
        stats['ships']      = len(self.spacecraft)

        return stats

    def __repr__(self):
        return '<Player %s (%s)>' % (self.game_name, self.username)
