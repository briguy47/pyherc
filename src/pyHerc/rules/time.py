#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

import os, sys
import logging
import pyHerc.data.model

__logger = logging.getLogger('pyHerc.rules.time')

def getNextCreature(model):
    """
    Get the character who is next to take action
    Returns
        Character
    """
    assert(model != None)

    level = model.player.level
    creatures = level.creatures[:]
    creatures.append(model.player)

    while 1:
        for creature in creatures:
            if creature.tick <= 0:
                return creature

        for creature in creatures:
            creature.tick = creature.tick - 1

def getNewTick(character, cost):
    """
    Calculate new tick for character
    Parameters:
        character : character performing the action
        cost : cost of the action
    Returns:
        new tick
    """
    assert(character != None)
    assert(cost != None)

    return character.tick + (character.speed * cost)