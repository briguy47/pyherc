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

'''
Module for testing combat related rules
'''

from pyHerc.test import IntegrationTest
from pyHerc.rules.public import ActionFactory
from pyHerc.rules.public import AttackParameters
from pyHerc.rules.attack.factories import AttackFactory
from pyHerc.data.model import Character
from pyHerc.data.dungeon import Level
from pyHerc.data import tiles

class TestMeleeCombat():
    '''
    Class for testing melee combat related rules
    '''
    pass
