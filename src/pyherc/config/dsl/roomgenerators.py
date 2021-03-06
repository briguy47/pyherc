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
module for RoomGenerators
"""
from pyherc.generators.level.room.catacombs import CatacombsGenerator
from pyherc.generators.level.prototiles import FLOOR_NATURAL
from random import Random

class Catacombs(object):
    """
    Generator for catacombs
    """
    def __init__(self):
        super(Catacombs, self).__init__()
        self.floor_tile = 0
        self.empty_tile = 0
        self.rng = Random()
        self.locations = []

    def with_(self, parameter):
        if hasattr(parameter, 'count'):
            if parameter[0] == 'floor':
                self.floor_tile = parameter[1]

        elif hasattr(parameter, 'random'):
            self.rng = parameter

        return self

    def located_at(self, location):
        self.locations.append(location)
        return self

    def build(self):
        return CatacombsGenerator(floor_tile = self.floor_tile,
                                  empty_tile = self.empty_tile,
                                  level_types = self.locations,
                                  rng = self.rng)

def natural_floor():
    return ('floor', FLOOR_NATURAL)
