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

#   explanation written by Björn Bergström of the FOV algorithm used here can be found from:
#   http://roguebasin.roguelikedevelopment.org/index.php/FOV_using_recursive_shadowcasting
#
#   original implementation by Eric D. Burgess is from:
#   http://roguebasin.roguelikedevelopment.org/index.php/Python_shadowcasting_implementation

import pyHerc.data.tiles

import logging
import math

__logger = logging.getLogger('pyHerc.rules.los')

mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]

def is_blocked(loc_x, loc_y, level, character = None):
    '''
    Checks if given location should be considered blocking for character
    @param loc_x: x-coordinate on the map
    @param loc_y: y-coordinate on the map
    @param level: level
    @param character: character
    @returns: False if not blocking, otherwise True
    '''
    assert level != None

    if loc_x < 0 or loc_y < 0:
        return True

    if loc_x >= len(level.walls) or loc_y >= len(level.walls[0]):
        return True

    if level.get_wall_tile(loc_x, loc_y) != pyHerc.data.tiles.wall_empty:
        return True
    else:
        return False

def cast_light(cx, cy, row, start, end, radius, xx, xy, yx, yy, fov_matrix, level):
    ''''
    Recursive lightcasting function
    @returns: fov_matrix
    '''
    if start < end:
        return
    radius_squared = radius*radius
    for j in range(row, radius+1):
        dx, dy = -j-1, -j
        blocked = False
        while dx <= 0:
            dx += 1
            # Translate the dx, dy coordinates into map coordinates:
            X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
            # l_slope and r_slope store the slopes of the left and right
            # extremities of the square we're considering:
            l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                # Our light beam is touching this square; light it:
                if dx*dx + dy*dy < radius_squared:
                    #transform from map to light_matrix
                    fov_matrix[X][Y] = True
                if blocked:
                    # we're scanning a row of blocked squares:
                    if is_blocked(X, Y, level):
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if is_blocked(X, Y, level) and j < radius:
                        # This is a blocking square, start a child scan:
                        blocked = True
                        cast_light(cx, cy, j+1, start, l_slope,
                                            radius, xx, xy, yx, yy, fov_matrix, level)
                        new_start = r_slope
        # Row is scanned; do next row unless last square was blocked:
        if blocked:
            break

    return fov_matrix

def do_fov(x, y, radius, fov_matrix, level):
    '''
    Calculate lit squares from the given location and radius
    '''
    for oct in range(8):
        cast_light(x, y, 1, 1.0, 0.0, radius,
                            mult[0][oct], mult[1][oct],
                            mult[2][oct], mult[3][oct], fov_matrix, level)

    return fov_matrix

def get_fov_matrix(model, character, distance = 7):
    fov_matrix = []

    width = len(character.level.walls[0])
    height = len(character.level.walls)

    for i in range(height):
        fov_matrix.append([False] * width)

    fov_matrix[character.location[0]][character.location[1]] = True

    return do_fov(character.location[0],
                  character.location[1], distance,
                  fov_matrix, character.level)
