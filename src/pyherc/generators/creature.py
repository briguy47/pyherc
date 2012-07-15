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
Module for creature generation related classes

Classes:
    CreatureGenerator
"""
from pyherc.ai import FlockingHerbivore
from pyherc.data import Character, EffectsCollection
from pyherc.rules.effects import EffectHandle
from pyherc.aspects import Logged
import random

class NewCreatureGenerator(object):
    """
    Class used to generate creatures
    """
    logged = Logged()

    @logged
    def __init__(self, configuration, model, action_factory, rng):
        """
        Default constructor
        """
        super(NewCreatureGenerator, self).__init__()
        self.configuration = configuration
        self.model = model
        self.action_factory = action_factory
        self.rng = rng

    @logged
    def generate_creature(self, name):
        """
        Generate creature

        :param name: name of the creature to generate
        :type name: string
        """
        config = self.__get_creature_config(name)

        new_creature = Character(self.model,
                                 self.action_factory,
                                 EffectsCollection(),
                                 self.rng)

        new_creature.name = config.name
        new_creature.body = config.body
        new_creature.finesse = config.finesse
        new_creature.mind = config.mind
        new_creature.hp = config.hp
        new_creature.speed = config.speed
        new_creature.icons = config.icons
        new_creature.attack = config.attack

        for spec in config.effect_handles:
            new_handle = EffectHandle(trigger = spec.trigger,
                                       effect = spec.effect,
                                       parameters = spec.parameters,
                                       charges = spec.charges)

            new_creature.add_effect_handle(new_handle)

        if not config.ai == None:
            new_creature.artificial_intelligence = config.ai(new_creature)

        return new_creature

    @logged
    def __get_creature_config(self, name):
        """
        Get creature config

        :param name: name of the creature
        :type name: string
        """
        return self.configuration.get_by_name(name)

class CreatureConfigurations(object):
    """
    Collection of creature configurations
    """
    logged = Logged()

    @logged
    def __init__(self, rng):
        """
        Default constructor

        :param rng: random number generator
        :type rng: Random
        """
        self.rng = rng
        self.creatures = {}

    @logged
    def add_creature(self, specification):
        """
        Add creature to configuration

        :param specification: specification of creature
        :type specification: CreatureConfiguration
        """
        self.creatures[specification.name] = specification

    @logged
    def get_by_name(self, name):
        """
        Get creature configuration

        :param name: name of the creature
        :type name: string
        """
        return self.creatures[name]

class CreatureConfiguration(object):
    """
    Configuration for an creature
    """

    def __init__(self, name, body, finesse, mind, hp, speed, icons, attack,
                 ai = None, effect_handles = None):
        """
        Default constructor
        """
        self.name = name
        self.body = body
        self.finesse = finesse
        self.mind = mind
        self.hp = hp
        self.speed = speed
        self.icons = icons
        self.attack = attack
        self.ai = ai

        if effect_handles == None:
            self.effect_handles = []
        else:
            self.effect_handles = effect_handles



class CreatureGenerator(object):
    """
    Class used to generate creatures
    """
    logged = Logged()

    @logged
    def __init__(self, model, action_factory, tables, rng):
        """
        Default constructor

        :param action_factory: Initialised action factory
        :type action_factory: ActionFactory
        :param tables: Tables defining creatures
        """
        self.model = model
        self.action_factory = action_factory
        self.tables = tables
        self.rng = rng

    @logged
    def generate_creature(self, parameters):
        """
        Generates a creature

        :param parameters: hash table containing parameters
        :type parameters: dict
        :returns: generated creature
        :rtype: Character
        """
        new_creature = None
        if not parameters == None:
            if 'name' in parameters.keys():
                table = self.tables.creatures[parameters['name']]
                new_creature = self.generate_creature_from_table(table)
        else:
            #generate completely random creature
            pass

        assert new_creature != None, 'Creature generation failed'
        return new_creature

    @logged
    def generate_creature_from_table(self, table):
        """
        Take table entry and generate corresponding creature
        """
        assert(table != None)

        new_creature = Character(self.model,
                                 self.action_factory,
                                 EffectsCollection(),
                                 self.rng)
        new_creature.name = table['name']
        new_creature.body = table['body']
        new_creature.finesse = table['finesse']
        new_creature.mind = table['mind']
        new_creature.hit_points = table['hp']
        new_creature.speed = table['speed']
        new_creature.size = table['size']
        new_creature.attack = table['attack']
        new_creature.artificial_intelligence = FlockingHerbivore(new_creature)

        if hasattr(table['icon'], 'append'):
            #select from list
            new_creature.icon = random.choice(table['icon'])
        else:
            new_creature.icon = table['icon']

        if 'effecthandles' in table.keys():
            for handle in table['effecthandles']:
                new_creature.add_effect_handle(
                                EffectHandle(trigger = handle.trigger,
                                             effect = handle.effect,
                                             parameters = handle.parameters,
                                             charges = handle.charges))

        assert new_creature != None, 'creature generation failed'
        return new_creature
