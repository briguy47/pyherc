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
import time
import pyHerc.data.model
import pyHerc.data.tiles

__logger = logging.getLogger('pyHerc.rules.moving')

def move(model, character, direction):
    """
    moves character to specified direction
    @param model: model of the world
    @param character: character to move
    @param direction: direction to move (1: north, 3: east, 9 enter portal)
    @note: Character does not move if it's not possible
    """
    assert(not model == None)
    assert(not character == None)
    assert(direction >= 1 and direction <= 10)

    __logger.debug('character ' + character.name +
                            ' moving from ' + character.location.__str__() +
                            ' to direction: ' + direction.__str__())

    event = {}
    event['type'] = 'moving'
    event['character'] = character
    event['location'] = character.location
    event['level'] = character.level

    moveData = check_move(model, character, direction)

    if moveData['ok'] == 1:
        character.location = moveData['location']
        character.level = moveData['level']
        character.tick = time.get_new_tick(character, 2)
        event['end location'] = character.location
        event['end level'] = character.level
        model.raise_event(event)

    __logger.debug('move finished at ' + character.location.__str__())

def check_move(model, character, direction):
    """
    checks if character can move to specific direction
    @param model: model of the world
    @param character: character to move
    @param direction: direction to move (1: north, 3: east, 9 enter portal)
    @return: dictionary with keys: location, level, ok
    """
    assert(not model == None)
    assert(not character == None)
    assert(direction >= 1 and direction <= 9)

    locationData = calculate_new_location(model, character, direction)

    if 'location' in locationData.keys() and 'level' in locationData.keys():
        newLocation = locationData['location']
        newLevel = locationData['level']

        if newLevel != None:
            if newLevel.walls[newLocation[0]][newLocation[1]] == pyHerc.data.tiles.wall_empty:
                #check for other creatures and such
                locationData['ok'] = 1
                creatures = newLevel.creatures[:]
                if model.player != None:
                    creatures.append(model.player)
                for creature in creatures:
                    if creature.location == newLocation:
                        locationData['ok'] = 0
            else:
                locationData['ok'] = 0
        else:
            #is this player escaping?
            if character == model.player:
                model.player.location = ()
                model.player.level = None
                model.end_condition = 1
                locationData['ok'] = 1
            else:
                locationData['ok'] = 0
    else:
        locationData['ok'] = 0

    return locationData

def calculate_new_location(model, character, direction):
    """
    Calculate new location if moving from old to certain direction
    @param character: character who is about to move
    @param direction: direction to move
    @param model: model to use
    @return: dictionary with keys: level, location
    """
    assert(character != None)
    assert(direction >= 1 and direction <= 9)
    assert(character.level != None)
    location = character.location
    newLevel = character.level

    if direction == 1:
        newLocation = (location[0], location[1] - 1)
    elif direction == 2:
        newLocation = (location[0] + 1, location[1] - 1)
    elif direction == 3:
        newLocation = (location[0] + 1, location[1])
    elif direction == 4:
        newLocation = (location[0] + 1, location[1] + 1)
    elif direction == 5:
        newLocation = (location[0], location[1] + 1)
    elif direction == 6:
        newLocation = (location[0] - 1, location[1] + 1)
    elif direction == 7:
        newLocation = (location[0] - 1, location[1])
    elif direction == 8:
        newLocation = (location[0] - 1, location[1] - 1)
    elif direction == 9:
        portal = newLevel.get_portal_at(location)
        if portal != None:
            if portal.getOtherEnd() != None:
                newLevel = portal.getOtherEnd().level
                newLocation = portal.getOtherEnd().location
            else:
                #proxy
                if portal.levelGenerator != None:
                    portal.generateLevel(model)
                    newLevel = portal.getOtherEnd().level
                    newLocation = portal.getOtherEnd().location
                else:
                    #escaping perhaps?
                    newLevel = None
                    newLocation = None
        else:
            return {}

    return {'location':newLocation,
                'level':newLevel}
