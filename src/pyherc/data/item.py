#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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

'''
Module for item related classes

Classes:
    Item
    WeaponData
    ItemEffectData
'''

import collections

class Item(object):
    """
    Represents item
    """

    def __init__(self):
        #attributes
        self.name = 'prototype'
        self.appearance = ''
        self.quest_item = 0
        #location
        self.location = ()
        self.level = None
        #icon
        self.icon = None
        self.weapon_data = None
        self.effects = None
        self.weight = None
        self.charges = None
        self.rarity = None
        self.cost = None
        self.tags = {}

    def __str__(self):
        return self.name

    def get_name(self, character, decorate = False):
        """
        Get name of the item
        Name can be appearance or given name
        @param character: character handling the item
        @param decorate: should name be decorated with status info, default False
        """
        assert character != None

        if self.appearance != '':
            if self.name in character.item_memory.keys():
                name = character.item_memory[self.name]
            else:
                name = self.appearance
        else:
            name = self.name

        if decorate == True:
            if self in character.weapons:
                name = name + ' (weapon in hand)'

        return name

    def add_effect(self, effect):
        '''
        Adds an effect to an item
        param effect: effect to add
        '''
        if self.effects == None:
            self.effects = {}

        if self.effects.has_key(effect.trigger):
            self.effects[effect.trigger].append(effect)
        else:
            self.effects[effect.trigger] = [effect]

    def get_effects(self, effect_type = None):
        '''
        Retrieves effects the item has
        Param effect_type: type of effects retrieved. Default None
        Returns: list of effects
        '''
        effect_list = []

        if self.effects != None:
            if effect_type == None:
                for trigger in self.effects.values():
                    effect_list = effect_list + trigger
            else:
                if self.effects.has_key(effect_type):
                    effect_list = effect_list + self.effects[effect_type]
                else:
                    effect_list = []

        return effect_list

    def charges_left(self):
        '''
        Returns amount of charges left in item
        In case of multiple charges, a list is returned
        '''
        if self.effects == None:
            return None

        effect_list = self.get_effects()

        amount_of_charges = [x.charges for x in effect_list]

        if len(amount_of_charges) == 1:
            return amount_of_charges[0]
        else:
            return amount_of_charges

    def maximum_charges_left(self):
        '''
        Return highest amount of charges left in item
        '''
        charges = self.charges_left()


        if charges != None:
            if isinstance(charges, collections.Sequence):
                if len(charges) > 0:
                    return max(charges)
                else:
                    return None
            else:
                return charges
        else:
            return None

    def minimum_charges_left(self):
        '''
        Return smallest amount of charges left in item
        '''
        charges = self.charges_left()

        if charges != None:
            return min(charges)
        else:
            return None

    def get_main_type(self):
        '''
        Return main type of the item
        '''
        main_type = 'undefined'

        if 'weapon' in self.tags:
            main_type = 'weapon'
        elif 'potion' in self.tags:
            main_type = 'potion'
        elif 'food' in self.tags:
            main_type = 'food'

        return main_type

    def get_tags(self):
        '''
        Return tags
        '''
        return self.tags

class WeaponData:
    '''
    Class representing weapon data of items
    '''
    def __init__(self, damage = None, damage_type = None, critical_range = None,
                 critical_damage = None, weapon_type = None):

        self.damage = damage
        self.damage_type = damage_type
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.weapon_type = weapon_type

class ItemEffectData:
    '''
    Represents magical effect on an item
    '''
    def __init__(self, trigger = None, effect_type = None,
                        power = None, charges = 1):

        self.trigger = trigger
        self.effect_type = effect_type
        self.power = power
        self.charges = charges
