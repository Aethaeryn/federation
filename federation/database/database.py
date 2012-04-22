# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''Uses SQLAlchemy to store data a SQL database.
'''
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

SEPARATOR = ', '
LOCATION  = 'sqlite:///:memory:'
Base      = declarative_base()

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

class Game(Base):
    '''Stores all of the information about a particular game running
    on the Federation server. The server should eventually have the
    capacity to run multiple game instances simultaneously with
    different settings between them.
    '''
    __tablename__ = 'game'

    id            = Column(Integer, primary_key=True)
    server_name   = Column(String(80), unique=True)
    start_year    = Column(Integer)
    turn          = Column(Integer)
    turns_per_day = Column(Integer)

    def __init__(self, server_name, start_year, turns_per_day):
        self.server_name   = server_name
        self.start_year    = start_year
        self.turns_per_day = turns_per_day
        self.turn          = 0

    def get_date(self):
        '''Converts the turn number into a calendar date. Each month is
        represented by an index on the list 'months'. An Earth calendar is
        used such that every 12 turns is a year, and each year has 12 months.
        '''
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

    fleet_id    = Column(Integer, ForeignKey('fleet.id'))
    map_id      = Column(Integer, ForeignKey('map.id'))
    owner_id    = Column(Integer, ForeignKey('player.id'))
    fleet       = relationship('Fleet', backref=backref('spacecraft', order_by=id))
    location    = relationship('Map', backref=backref('spacecraft', order_by=id))
    owner       = relationship('Player', backref=backref('spacecraft', order_by=id))

    x_position  = Column(Integer)
    y_position  = Column(Integer)

    def __init__(self, name, custom_name, owner):
        self.name        = name
        self.custom_name = custom_name
        self.owner       = owner

    def __repr__(self):
        return '<Spacecraft %s (%s)>' % (self.custom_name, self.name)

class Federation(Base):
    '''Federations are similar to clans, factions, alliances, teams,
    etc., in various other games. These are voluntary collections of
    players who are on the same side and friendly to each other, with
    common aims.

    Like governments, federations can have leaders and can implement
    certain political policies.
    '''
    __tablename__ = 'federation'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80), unique=True)
    cash        = Column(Integer)
    date        = Column(DateTime)
    shared_view = Column(Boolean)
    tax_rate    = Column(Integer)

    def __init__(self, name, founder):
        self.name    = name
        self.founder = founder
        self.date    = datetime.utcnow()

    def __repr__(self):
        return '<Federation %s>' % (self.name)

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
        '''Returns the information that the UI expects.
        '''
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
    '''Fleets are a collection of ships that are held together under
    the command of one or two players.
    '''
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
    '''Units are individual humanoids that can be hired in the game
    for various purposes.
    '''
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
    '''Bodies are all celestial territories: asteroid belts, planets,
    moons, stars, etc.
    '''
    __tablename__ = 'body'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(80))
    custom_name = Column(String(80))
    variant     = Column(String(80))

    map_id      = Column(Integer, ForeignKey('map.id'))
    owner_id    = Column(Integer, ForeignKey('player.id'))
    location    = relationship('Map', backref=backref('bodies', order_by=id))
    owner       = relationship('Player', backref=backref('territory', order_by=id))

    x_position  = Column(Integer)
    y_position  = Column(Integer)

    def __init__(self, name, custom_name, variant):
        self.name        = name
        self.custom_name = custom_name
        self.variant     = variant

    def __repr__(self):
        return '<Body %s (%s %s)>' % (self.custom_name, self.name, self.id)

class Structure(Base):
    '''Structures are buildings built on a body that modify its
    capabilities, similar to components on a spacecraft.
    '''
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
        stats = (self.name, self.id, self.body.custom_name, self.body.id)
        return '<Structure %s %s (%s %s)>' % stats

class Map(Base):
    '''A map is a way for the player to interact with the game world
    by rendering a hex-based representation of the various items that
    have a definite location.

    Maps are either detailed views of star systems ('system') or broad
    overviews of clusters of stars ('sector').
    '''
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
        self.x_position = x_pos
        self.y_position = y_pos
        self.map_type   = map_type

    def __repr__(self):
        stats = (self.map_type, self.name, self.x_size, self.y_size)
        return '<%s %s (%s x %s)>' % stats

class ModelBody(Base):
    '''This stores the general data of various classes of celestial
    bodies, used as a reference for specific bodies in the game.
    '''
    __tablename__ = 'model_body'

    id          = Column(Integer, primary_key = True)
    name        = Column(String(80))
    description = Column(String)
    variants    = Column(String)

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

        if 'variants' in dictionary:
            self.variants = SEPARATOR.join(self.variants)

    def __repr__(self):
        return '<Body %s Model>' % (self.name)

class ModelUnit(Base):
    '''This stores the general data of various types of units and the
    stats they have.
    '''
    __tablename__ = 'model_unit'

    id          = Column(Integer, primary_key = True)
    name        = Column(String(80))
    cost        = Column(Integer)
    damage      = Column(Integer)
    description = Column(String)
    hitpoints   = Column(Integer)
    special     = Column(Integer)

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    def __repr__(self):
        return '<Unit %s Model>' % (self.name)

class ModelStructure(Base):
    '''These are the general structure stats.
    '''
    __tablename__ = 'model_structure'

    id          = Column(Integer, primary_key = True)
    name        = Column(String(80))
    cost        = Column(Integer)
    description = Column(String)
    hitpoints   = Column(Integer)
    shields     = Column(Integer)
    special     = Column(String)
    wep_damage  = Column(Integer)
    wep_special = Column(String)
    wep_speed   = Column(Integer)
    wep_type    = Column(String)

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    def __repr__(self):
        return '<Structure %s Model>' % (self.name)

class ModelSpacecraft(Base):
    '''This contains information about each general spacecraft type
    that is purchasable by the player.
    '''
    __tablename__ = 'model_spacecraft'

    id             = Column(Integer, primary_key = True)
    name           = Column(String(80))
    base_cost      = Column(Integer)
    component_list = Column(String)
    component_max  = Column(Integer)
    description    = Column(String)
    inherits       = Column(String)
    size           = Column(String)
    special        = Column(String)

    def __init__(self, dictionary):
        required = set(['name', 'description', 'size', 'base_cost',
                        'component_list', 'component_max'])

        for item in required:
            if item not in dictionary and 'inherits' not in dictionary:
                raise Exception('Entry %s not in spacecraft definition!' % item)

        self.__dict__.update(dictionary)

        self.component_list = SEPARATOR.join(self.component_list)

    def get_full_stats(self):
        '''Gives the actual spacecraft stats by using the component
        stats for every component in the component list.
        '''
        components = self.component_list.split(SEPARATOR)

        stats = {'cargo'         : 0,
                 'components_in' : 0,
                 'crew'          : 0,
                 'dock'          : 0,
                 'hitpoints'     : 0,
                 'hyperspace'    : False,
                 'sensors'       : 0,
                 'shields'       : 0,
                 'speed'         : 0,
                 'value'         : self.base_cost}

        for component in components:
            stats = self._add_component(component, stats)

    def _add_component(self, component, stats):
        '''Adds a particular component's stats to the spacecraft's stats.
        '''
        #### TODO get component stats from the ModelComponent

        stats["components_in"] += component.exp_size
        stats["value"]         += component.cost

        #### TODO imported from environment.py : get to work here!
        # for stat in dir(component):
        #     if stat in stats:
        #         value = component.__dict__[stat]
        #
        #         if type(value) is int:
        #             self.__dict__[stat] += value
        #
        #         if value and type(value) is bool:
        #             self.__dict__[stat] = True

        return stats

    def __repr__(self):
        return '<Spacecraft %s Model>' % (self.name)

class ModelComponent(Base):
    '''ModelComponents contain all of the stats general to component
    types rather than specific to a particular instance of components.
    '''
    __tablename__ = 'model_component'

    id          = Column(Integer, primary_key = True)
    name        = Column(String(80))
    cost        = Column(Integer)
    description = Column(String)
    size        = Column(String)

    cargo       = Column(Integer)
    crew        = Column(Integer)
    dock        = Column(Integer)
    hitpoints   = Column(Integer)
    hyperspace  = Column(Boolean)
    sensors     = Column(Integer)
    shields     = Column(Integer)
    special     = Column(String)
    speed       = Column(Integer)
    unsellable  = Column(Boolean)
    wep_damage  = Column(Integer)
    wep_special = Column(Integer)
    wep_speed   = Column(Integer)
    wep_type    = Column(Integer)

    def __init__(self, dictionary):
        required = set(['name', 'description', 'size', 'cost'])

        for item in required:
            if item not in dictionary:
                raise Exception('Entry %s not in component definition!' % item)

        self.__dict__.update(dictionary)

        if 'hitpoints' not in dictionary:
            self.hitpoints = 0

        if self.size == 'Small Component':
            self.hitpoints += 5
            self.exp_size   = 1

        elif self.size == 'Medium Component':
            self.hitpoints += 10
            self.exp_size   = 2

        elif self.size == 'Large Component':
            self.hitpoints += 20
            self.exp_size   = 4

    def __repr__(self):
        return '<Component %s Model>' % (self.name)

db      = Database(LOCATION)
session = db.session

def debug():
    '''Temporary method that tests various parts of the database. This
    will eventually be replaced by a standalone test module.
    '''
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
    spaceships = ['Battle Frigate', 'Battle Frigate',
                  'Basic Fighter', 'Cruiser']

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
