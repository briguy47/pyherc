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
import time

__logger = logging.getLogger('pyHerc.rules.items')

def pickUp(model, character, item):
    """
    Pick up an item
    @param model: model to use
    @param character: character picking up the item
    @param item: item to be picked up
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)
    assert(item in character.level.items)

    __logger.debug(character.__str__() + ' picking up item: ' + item.__str__())

    event = {}
    event['type'] = 'item'
    event['pick up'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raiseEvent(event)

    character.level.items.remove(item)
    character.inventory.append(item)
    item.location = ()
    character.tick = time.getNewTick(character, 1.5)

    __logger.debug('item picked up')

def drop(model, character, item):
    """
    Drop item from inventory
    @param model: model to use
    @param character: character who is dropping the item
    @param item: item to be dropped
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)
    assert(item in character.inventory)

    __logger.debug(character.__str__() + ' dropping item ' + item.__str__())

    event = {}
    event['type'] = 'item'
    event['drop'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raiseEvent(event)

    character.level.addItem(item, character.location)
    character.inventory.remove(item)
    character.tick = time.getNewTick(character, 1.5)

    __logger.debug('item dropped')

def wield(model, character, item, dualWield = False):
    """
    Wield a weapon
    @param model: model to use
    @param character: character trying to wield the weapon
    @param item: weapon to wield
    @param dualWield: should character perform dual wield
    """
    __logger.debug(character.__str__() + ' wielding item ' + item.__str__())

    if len(character.weapons) == 0:
        #simple wield
        character.weapons.append(item)
        __logger.debug(character.__str__() + ' wielded item ' + item.__str__())
    else:
        #possible dual wield?
        if dualWield == True:
            if len(character.weapons) == 1:
                if canDualWield(model, character, character.weapons[0], item):
                    character.weapons.append(item)
                    __logger.debug(character.__str__() + ' dual-wielded item ' + item.__str__())
                    #TODO: feedback when wielding is not possible

def canDualWield(model, character, item1, item2):
    """
    Checks if character can dual-wield given items
    @param model: model to use
    @param character: character to try dual-wielding
    @param item1: item to wield
    @param item2: item to wield
    @return: 1 if can dual-wield, 0 otherwise
    """
    if dualWieldable(model, character, item1) and dualWieldable(model, character, item2):
        return 1
    else:
        return 0

def dualWieldable(model, character, item):
    """
    Checks if item is dual-wieldable for a character
    @param model: model to use
    @param character: character to try dual-wielding
    @param item: item to dual wield
    @return: 1 if can dual-wield, 0 otherwise
    """
    if ('one-handed weapon' in item.tags or 'light weapon' in item.tags):
        return 1
    else:
        return 0
