'''This file contains model objects in the database. These are things
that are read in at the start of a new game from static config files
and rarely, if ever, change. Their main role is to serve as a point of
reference for specific in-game instances that these models refer to.

If there is data that is held in common between all objects of some
type and the data never changes or changes for all of them at the same
time, then it probably should go here instead.

Note: One possible optimization (past the prototype stage) would be to
store these all in memory in dictionary form. This way, the game can
access it immediately without continuously reading from the disk, and
would only need to read from the database if something changes or if
the server is (re)starting.
'''
from federation.database import Base
from sqlalchemy import Column, Integer, Boolean, String

SEPARATOR = ', '

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
