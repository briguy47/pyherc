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
Classes for move events
"""
from pyherc.events.event import Event

class AttackHitEvent(Event):
    """
    Event that can be used to relay information about moving

    .. versionadded:: 0.4
    """
    def __init__(self, type, attacker, target, damage, hit,
                 affected_tiles):
        """
        Default constructor
        """
        super(AttackHitEvent, self).__init__(event_type = 'attack hit',
                                             level = attacker.level,
                                             location = attacker.location,
                                             affected_tiles = affected_tiles)

        self.type = type
        self.attacker = attacker
        self.target = target
        self.damage = damage
        self.hit = hit

    def get_description(self, point_of_view):
        """
        Description of the event

        :param point_of_view: point of view for description
        :type point_of_view: Character
        :returns: description of the event
        :rtype: string
        """
        if point_of_view == self.attacker:
           description = 'You hit {0}'.format(self.target.name)
        elif point_of_view == self.target:
            description = '{0} hits you'.format(self.attacker.name)
        else:
            description = '{0} hits {1}'.format(self.attacker.name,
                                                self.target.name)

        return description
