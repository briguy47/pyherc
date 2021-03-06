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
Module for proto tile IDs

These IDs are used to mark tiles on generated levels before the level has been
processed by decorator. This allows level generators to work on higher level of
abstraction and real theme of the level can be changed by using different
decorators.
"""

FLOOR_EMPTY = -1
FLOOR_NATURAL = -2
FLOOR_CONSTRUCTED = -3

WALL_EMPTY = -100
WALL_NATURAL = -101
WALL_CONSTRUCTED = -102
