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
Module for magic
"""

import logging
import pyherc.data.model
import pyherc.rules.utils

__logger = logging.getLogger('pyherc.rules.magic')

def cast_effect(target, effect, dice = None):
    """
    Casts effect of a spell, potion, etc. on a target

    Args:
        target: target of the effect
        effect: EffectHandle object
        dice: prerolled dice
    """
    assert(effect != None)

    __logger.info('casting effect: ' + effect.effect)

    if effect.effect in ('healing', 'damage'):
        cast_hp_effect(target, effect, dice)

def cast_hp_effect(target, effect, dice = None):
    """
    Casts HP effect on target, causing it to gain or lose some HP
    @param target: target of the effect
    @param effect: parameters of effect in dictionary
    @param dice: prerolled dice
    """
    hp_power = effect.power
    model = target.model
    if dice != None and len(dice) > 0:
        hp_roll = dice.pop()
        assert(hp_roll <= pyherc.rules.utils.get_max_score(hp_power))
    else:
        hp_roll = pyherc.rules.utils.roll_dice(hp_power)

    event = {}

    if effect.effect == 'healing':
        target.hit_points = target.hit_points + hp_roll
        event['type'] = 'magic heal'
    elif effect.effect == 'damage':
        target.hit_points = target.hit_points - hp_roll
        event['type'] = 'magic damage'

    if target.hit_points < 0:
        pyherc.rules.ending.check_dying(model, target, None)

    if target.hit_points > target.get_max_hp():
        target.hit_points = target.get_max_hp()

    event['character'] = target
    event['location'] = target.location
    event['level'] = target.level
    event['power'] = hp_roll

    model.raise_event(event)
