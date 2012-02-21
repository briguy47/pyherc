#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
#
#   This file is part of pyherc.
#
#   pyherc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyherc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

'''
Classs needed for generating levels
'''

import logging
import random
from pyherc.generators import ItemGenerator
from pyherc.generators import CreatureGenerator
from pyherc.data import Level

class LevelGeneratorFactory:
    '''
    Class used to contruct different kinds of level generators
    '''
    def __init__(self, action_factory, level_configurations):
        '''
        Default constructor

        @param action_factory: ActionFactory to pass to the generator
        @param level_configurations: List of LevelGeneratorConfiguration objects
        '''
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGeneratorFactory') #pylint: disable=c0301
        self.action_factory = action_factory
        self.level_configurations = level_configurations

    def get_generator(self, level, random_generator = random.Random()):
        '''
        Get LevelGenerator for given level
        @param level: current level (how deep player has reached)
        @param random_generator: Optional random number generator
        '''
        return LevelGenerator(self.action_factory,
                                        self.level_configurations[level - 1],
                                        random_generator)

class LevelGenerator:
    '''
    Class used to generate levels
    '''
    def __init__(self, action_factory, configuration, random_generator):
        '''
        Default constructor
        @param action_factory: ActionFactory instance
        @param configuration: LevelGeneratorConfiguration
        '''
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGenerator') #pylint: disable=C0301
        self.item_generator = ItemGenerator()
        self.creature_generator = CreatureGenerator(action_factory)
        self.random_generator = random_generator

        self.action_factory = action_factory
        self.level_partitioners = configuration.level_partitioners
        self.room_generators = configuration.room_generators

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGenerator') #pylint: disable=C0301

    def generate_level(self, portal, model, new_portals = 0,
                                        level=1, room_min_size = (2, 2)):
        '''
        Generate level
        '''
        self.logger.debug('creating a new level')
        new_level = Level((60, 40))

        self.logger.debug('partitioning level')
        partitioner = self.random_generator.choice(self.level_partitioners)
        sections = partitioner.partition_level(new_level, 4, 3)

        self.logger.debug('generating rooms')
        for section in sections:
            room_generator = self.random_generator.choice(self.room_generators)
            room_generator.generate_room(section)

        # decorate level
        # add stairs
        # add monsters
        # add items

        self.logger.debug(new_level.dump_string())

        return new_level