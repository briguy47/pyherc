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
Module for testing customer matchers
"""

from pyherc.data import Level
from pyherc.data.tiles import WALL_EMPTY, FLOOR_ROCK, WALL_GROUND
from pyherc.test.matchers import MapConnectivity
from hamcrest import * #pylint: disable=W0401

class TestLevelConnectivity():
    """
    Class for testing level connectivity matcher
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None

    def setup(self):
        """
        Setup the tests
        """
        self.level = Level(size = (10, 10),
                      floor_type = FLOOR_ROCK,
                      wall_type = WALL_GROUND)
    def test_unconnected_level(self):
        """
        Test that unconnected level is reported correctly
        """
        for loc_x in range(2, 5):
            self.level.walls[loc_x][2] = WALL_EMPTY
            self.level.walls[loc_x][5] = WALL_EMPTY

        matcher = MapConnectivity(self.level)

        assert_that(matcher._matches(True), is_(equal_to(False)))

    def test_connected_level(self):
        """
        Test that connected level is reported correctly
        """
        for loc_x in range(2, 8):
            self.level.walls[loc_x][3] = WALL_EMPTY
            self.level.walls[loc_x][5] = WALL_EMPTY
            self.level.walls[5][loc_x] = WALL_EMPTY

        matcher = MapConnectivity(self.level)

        assert_that(matcher._matches(True), is_(equal_to(True)))
