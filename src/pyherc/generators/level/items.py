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
Classes for item generation
"""
class ItemAdderConfiguration(object):
    """
    Configuration for ItemAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        super(ItemAdderConfiguration, self).__init__()
        self.items = []

    def add_item(self, min_amount, max_amount, name = None, type = None,
                 location = None):
        """
        Adds item to configuration

        Args:
            item: specification for item
        """
        item_spec = {}
        item_spec['min_amount'] = min_amount
        item_spec['max_amount'] = max_amount
        item_spec['name'] = name
        item_spec['type'] = type
        item_spec['location'] = location

        self.items.append(item_spec)


class ItemAdder(object):
    """
    Class for adding items
    """
    def __init__(self, item_generator, configuration, rng):
        """
        Default constructor

        Args:
            item_generator: ItemGenerator instance
            configuration: ItemAdderConfiguration
            rng: random number generator
        """
        super(ItemAdder, self).__init__()
        self.item_generator = item_generator
        self.configuration = configuration
        self.rng = rng

    def add_items(self, level):
        """
        Add items

        Args:
            level: Level to add items
        """
        item_list = self.configuration.items
        items = []

        for item in item_list:
            items.extend(self.generate_items(item))

        self.place_items(items, level)

    def generate_items(self, item_spec):
        """
        Generate items according to specification

        Args:
            item_spec: Dictionary specifying items to create

        Returns
            tupple (item_spec, item)
            where item_spec is specification used to generate item
            and item is generated Item
        """
        amount = self.rng.randint(item_spec['min_amount'],
                                  item_spec['max_amount'])

        return []

    def place_items(self, items, level):
        """
        Place items to level

        Args:
            item: list of tupples (item_spec, item)
            level: level to place items
        """
        pass
