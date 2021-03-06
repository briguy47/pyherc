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
Module for Model related classes
"""

import logging
from pyherc.aspects import Logged

class Model(object):
    """
    Represents playing world
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Default constructor
        """
        self.dungeon = None
        self.player = None
        self.config = None
        self.tables = None
        self.__event_listeners = []
        self.end_condition = 0
        self.logger = logging.getLogger('pyherc.data.model.Model')

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.model.Model')

    @logged
    def register_event_listener(self, listener):
        """
        Registers event listener on this model

        :param listener: Listener to register
        """
        assert listener != None
        self.__event_listeners.append(listener)

    @logged
    def get_event_listeners(self):
        """
        Retrieve registered event listeners
        """
        return self.__event_listeners[:]

    @logged
    def raise_event(self, event):
        """
        Relays event to creatures

        :param event: event to relay
        :type event: dict
        """
        level = event.level

        if level != None:
            for creature in level.creatures:
                creature.receive_event(event)

        for listener in self.__event_listeners:
            listener.receive_event(event)

    def get_next_creature(self):
        """
        Get the character who is next to take action

        :returns: Character to act next
        :rtype: Character
        """
        level = self.player.level
        creatures = level.creatures

        assert len(creatures) != 0
        assert self.player in level.creatures

        while 1:
            for creature in creatures:
                if creature.tick <= 0:
                    return creature

            for creature in creatures:
                creature.tick = creature.tick - 1
                for effect in creature.get_effects():
                    effect.tick = effect.tick - 1
                    if effect.tick == 0:
                        effect.trigger()
                creature.remove_expired_effects()

class Damage(object):
    """
    Damage done in combat
    """
    def __init__(self, amount = 0, damage_type = 'bludgeoning',
                        magic_bonus = 0):
        self.amount = amount
        self.damage_type = damage_type
        self.magic_bonus = magic_bonus

class MimicData():
    """
    Represents mimicing character
    """
    def __init__(self, character):
        self.fov_matrix = []
        self.character = character

    def get_character(self):
        """
        Get mimicing character

        :returns: Character
        :rtype: Character
        """
        return self.character

    def set_character(self, character):
        """
        Set character mimicing this item

        :param character: Character to set
        :type character: Character
        """
        self.character = character
