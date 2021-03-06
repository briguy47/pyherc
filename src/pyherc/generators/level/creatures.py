#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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

"""
Classes for creature generation
"""

from pyherc.aspects import Logged

class CreatureAdderConfiguration(object):
    """
    Class used to configure CreatureAdder
    """
    logged = Logged()

    @logged
    def __init__(self, level_types):
        """
        Default constructor

        :param level_types: types of levels adder can be used at
        :type level_types: [string]
        """
        super(CreatureAdderConfiguration, self).__init__()
        self.level_types = level_types
        self.creature_list = []

    @logged
    def add_creature(self, min_amount, max_amount, name, location = None):
        """
        Adds creature specification

        :param min_amount: minimum amount of creatures to generate
        :type min_amount: integer
        :param max_amount: maximum amount of creatures to generate
        :type max_amount: integer
        :param name: name of the creature to generate
        :type name: string
        :param location: location type where creature is placed
        :type location: string
        """
        config_item = {}
        config_item['min_amount'] = min_amount
        config_item['max_amount'] = max_amount
        config_item['name'] = name
        config_item['location'] = location

        self.creature_list.append(config_item)

class CreatureAdder(object):
    """
    Class used to add creatures during level generation
    """
    logged = Logged()

    @logged
    def __init__(self, creature_generator, configuration, rng):
        """
        Default constructor

        :param creature_generator: creature generator used to create creatures
        :type creature_generator: CreatureGenerator
        :param configuration: configuration
        :type configuration: CreatureAdderConfiguration
        :param rng: random number generator
        :type rng: Random
        """
        super(CreatureAdder, self).__init__()
        self.creature_generator = creature_generator
        self.configuration = configuration
        self.rng = rng

    @logged
    def __get_level_types(self):
        """
        Get level types this adder can be used at

        :returns: level types this adder can be used at
        :rtype: [string]
        """
        return self.configuration.level_types

    @logged
    def add_creatures(self, level):
        """
        Add creatures to level according to configuration

        :param level: level to add creatures
        :type level: Level
        """
        creature_list = self.configuration.creature_list
        creatures = []

        for creature in creature_list:
            amount = self.rng.randint(creature['min_amount'],
                                      creature['max_amount'])
            creatures.extend(self.generate_creatures(creature['name'],
                                                     amount))

        self.place_creatures(creatures, creature_list, level)

    @logged
    def generate_creatures(self, name, amount):
        """
        Generate creatures

        :param name: name of the creatures to generate
        :type name: string
        :param amount: amount of creatures to generate
        :type amount: integer
        :returns: generated creatures
        :rtype: [Character]
        """
        creatures = []
        for i in range(amount):
            new_creature = self.creature_generator.generate_creature(name)
            creatures.append(new_creature)

        return creatures

    @logged
    def place_creatures(self, creatures, creature_list, level):
        """
        Place creatures into a level

        :param creatures: creatures to place
        :type creatures: [Character]
        :param creature_list: specification where to place creatures
        :type creature_list: dict
        :param level: level to place creatures
        :type level: Level
        """
        for creature in creatures:
            location_type = [x['location'] for x in creature_list
                             if x['name'] == creature.name]

            if location_type == None:
                location_type = 'any'

            locations = level.get_locations_by_type('room')

            location = self.rng.choice(locations)

            level.add_creature(creature, location)

    level_types = property(__get_level_types)

