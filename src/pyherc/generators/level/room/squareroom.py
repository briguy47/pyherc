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
Classes for generating square rooms
"""

import logging
from pyherc.generators.level.room.corridor import CorridorGenerator

class SquareRoomGenerator(object):
    """
    Class for generating a square room
    """
    def __init__(self, floor_tile, empty_tile, level_types):
        """
        Default constructor

        :param floor_tile: id of the tile to use for floors
        :type floor_tile: integer
        :param empty_tile: id of the empty wall tile
        :type empty_tile: integer
        :param level_types: types of level this generator can be used
        :type level_types: [string]
        """
        self.floor_tile = floor_tile
        self.empty_tile = empty_tile
        self.room_width = None
        self.room_height = None
        self.level_types = level_types
        self.logger = logging.getLogger('pyherc.generators.level.room.squareroom.SquareRoomGenerator') #pylint disable=C0301

    def generate_room(self, section):
        """
        Generate room

        :param section: section for generator to draw to
        :type section: Section
        """

        self.room_width = int(section.width * 0.50)
        self.room_height = int(section.height * 0.50)

        room_left_edge = (section.width - self.room_width) // 2
        room_right_edge = room_left_edge + self.room_width
        room_top_edge = (section.height - self.room_height) // 2
        room_bottom_edge = room_top_edge + self.room_height

        for loc_y in range(room_top_edge + 1, room_bottom_edge):
            for loc_x in range(room_left_edge + 1, room_right_edge):
                section.set_floor((loc_x, loc_y), self.floor_tile, 'room')
                section.set_wall((loc_x, loc_y), self.empty_tile, None)

        center_x = (room_right_edge - room_left_edge) // 2 + room_left_edge
        center_y = (room_bottom_edge - room_top_edge) // 2 + room_top_edge

        section.add_room_connection((center_x, room_top_edge), "up")
        section.add_room_connection((center_x, room_bottom_edge), "down")
        section.add_room_connection((room_left_edge, center_y), "left")
        section.add_room_connection((room_right_edge, center_y), "right")

        self.add_corridors(section)

    def add_corridors(self, section):
        """
        Add corridors leading from room connection to section connections

        :param section: section to add corridors
        :type section: Section
        """
        for section_connection in section.connections:
            room_connection = self.find_room_connection(section,
                                                        section_connection)
            corridor = CorridorGenerator(
                                room_connection,
                                section_connection.translate_to_section(),
                                self.empty_tile)
            corridor.generate()

    def find_room_connection(self, section, section_connection):
        """
        Find room connection that matches to given section connection

        :param section: section to handle
        :type section: Section
        :param section_connection: connection at the edge of section
        :type section_connection: Connection
        :returns: matching room connection
        :rtype: Connection
        """
        return section.find_room_connection(section_connection)
