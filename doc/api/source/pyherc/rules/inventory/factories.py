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
Inventory manipulation related factories are defined here
"""
import types
from pyherc.rules.inventory.action import PickUpAction
from pyherc.rules.factory import SubActionFactory
from pyherc.aspects import Logged

class PickUpFactory(SubActionFactory):
    """
    Factory for creating pick up actions
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Constructor for this factory
        """
        self.sub_action = 'pick up'

    @logged
    def can_handle(self, parameters):
        """
        Can this factory process these parameters

        :param parameters: parameters to check
        :returns: True if factory is capable of handling parameters
        :rtype: Boolean
        """
        return self.sub_action == parameters.sub_action

    @logged
    def get_action(self, parameters):
        """
        Create a pick up action

        :param parameters: parameters used to control creation
        :type parameters: InventoryParameters
        """
        return PickUpAction(parameters.character, parameters.item)

class InventoryFactory(SubActionFactory):
    """
    Factory for constructing inventory actions
    """
    logged = Logged()

    @logged
    def __init__(self, factories):
        """
        Constructor for this factory

        :param factories: a single Factory or list of Factories to use
        :type factories: SubActionFactory or [SubActionFactory]
        """
        self.action_type = 'inventory'

        if isinstance(factories, types.ListType):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)
