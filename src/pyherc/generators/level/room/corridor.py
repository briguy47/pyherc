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

"""
Classes for generating corridors
"""

import logging

class CorridorGenerator(object):
    """
    Class for making simple corridors
    """
    def __init__(self, start_point, end_point, tile):
        """
        Default constructor

        Args:
            start_point: (loc_x, loc_y) starting location
            end_point: (loc_x, loc_y) ending location
            tile: ID of tile to place
        """
        object.__init__(self)
        self.start_point = start_point
        self.end_point = end_point
        self.tile = tile

    def generate(self):
        """
        Carves corridor from start_point to end_point
        """
        if self.start_point.location[1] == self.end_point.location[1]:
            self.__carve_horizontal()

    def __carve_horizontal(self):
        """
        Special case, carving is done in straigth horizontal line
        """
        if self.start_point.location[0] > self.end_point.location[0]:
            start_x = self.end_point.location[0]
            end_x = self.start_point.location[0]
        else:
            start_x = self.start_point.location[0]
            end_x = self.end_point.location[0]

        y_loc = self.start_point.location[1]
        section = self.start_point.section

        for x_loc in range(start_x, end_x):
            section.set_wall((x_loc, y_loc), self.tile)
