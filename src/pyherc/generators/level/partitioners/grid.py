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
Module for partitioning level to equal grid
"""

import logging
from pyherc.generators.level.partitioners.section import Section
from pyherc.aspects import Logged

class RandomConnector(object):
    """
    Class for building random connection network from sections
    """
    logged = Logged()

    @logged
    def __init__(self, random_generator):
        """
        Default constructor

        :param random_generator: random number generator
        :type random_generator: Random
        """
        self.random_generator = random_generator
        self.logger = logging.getLogger('pyherc.generators.level.partitioners.grid.RandomConnector') #pylint: disable=C0301

    @logged
    def connect_sections(self, sections, start_section = None):
        """
        Connects sections together

        :param sections: sections to connect
        :type sections: [Section]
        :param start_section: optional parameter specifying starting section
        :type start_section: Section
        """
        if start_section == None:
            start_location = self.random_generator.choice(sections)
        else:
            start_location = start_section

        self.form_path_from_sections(start_location, sections)

        if len(sections) > 1:
            unconnected_sections = [x for x in sections
                                if x.connected == False]

            while len(unconnected_sections) > 0:
                edge_sections = [x for x in sections
                                if x.connected == True
                                and x.has_unconnected_neighbours()]

                start_location = self.random_generator.choice(edge_sections)

                self.form_path_from_sections(start_location, sections)

                unconnected_sections = [x for x in sections
                                        if x.connected == False]

        return sections

    @logged
    def form_path_from_sections(self, start_section, sections):
        """
        Builds path of connected sections

        :param start_section: section to start connecting from
        :type start_section: Section
        :param sections: sections to connect
        :type sections: [Section]
        """
        current_section = start_section
        unconnected_neighbours = [x for x in current_section.neighbours
                                                if x.connected == False]

        while len(unconnected_neighbours) > 0:
            next_section = self.random_generator.choice(
                                                unconnected_neighbours)

            current_section.connect_to(next_section)

            current_section = next_section
            unconnected_neighbours = [x for x in current_section.neighbours
                                                if x.connected == False]


class GridPartitioner(object):
    """
    Class for partitioning level to equal grid
    """
    logged = Logged()

    @logged
    def __init__(self, level_types, x_sections,  y_sections, random_generator):
        """
        Default constructor

        :param level_types: types of level partitioner can be used for
        :type level_types: [string]
        :param x_sections: amount of sections to split horizontally
        :type x_sections: integer
        :param y_sections: amount of sections to split vertically
        :type y_sections: integer
        :param random_generator: random number generator
        :type random_generator: Random
        """
        self.connectors = [RandomConnector(random_generator)]
        self.level_types = level_types
        self.x_sections = x_sections
        self.y_sections = y_sections
        self.random_generator = random_generator

    @logged
    def partition_level(self, level):
        """
        Creates partitioning for a given level with connection points

        :param level: level to partition
        :type level: Level
        :returns: connected sections
        :rtype: [Section]
        """
        sections = []
        section_matrix = [[None for i in range(self.y_sections)]
                                               for j in range(self.x_sections)]
        size_of_level = level.get_size()

        x_sections = self.split_range_to_equals(size_of_level[0],
                                                self.x_sections)
        y_sections = self.split_range_to_equals(size_of_level[1],
                                                self.y_sections)

        for y_block in range(len(y_sections)):
            for x_block in range(len(x_sections)):
                temp_section = Section(
                                       (x_sections[x_block][0],
                                        y_sections[y_block][0]),
                                        (x_sections[x_block][1],
                                        y_sections[y_block][1]),
                                        level,
                                        self.random_generator)

                self.connect_new_section(temp_section,
                                         (x_block, y_block),
                                         section_matrix)
                section_matrix[x_block][y_block] = temp_section
                sections.append(temp_section)

        connector = self.random_generator.choice(self.connectors)
        connected_sections = connector.connect_sections(sections)

        return connected_sections

    @logged
    def connect_new_section(self, section, location, sections):
        """
        Connects section in given location to its neighbours

        :param section: section to connect
        :type section: Section
        :param location: location of the section
        :param sections: sections
        :type sections: [Section]
        """
        if location[0] > 0:
            left_section = sections[location[0]-1][location[1]]
            left_section.neighbours.append(section)
            section.neighbours.append(left_section)

        if location[1] > 0:
            up_section = sections[location[0]][location[1]-1]
            up_section.neighbours.append(section)
            section.neighbours.append(up_section)

    @logged
    def split_range_to_equals(self, length, sections):
        """
        Split range into equal sized chunks

        :param length: range to split
        :type length: integer
        :param sections: amount of sections to split
        :type sections: integer
        :returns: list containing end points of chunks
        :rtype: [integer]
        """
        section_length = length // sections
        ranges = []

        for i in range(sections):
            ranges.append((i * section_length, (i + 1) * section_length - 1))

        return ranges
