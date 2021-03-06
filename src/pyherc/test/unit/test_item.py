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
Module for classes testing Item related operations
"""
#pylint: disable=W0614
import pyherc
import pyherc.generators.item
import pyherc.data.dungeon
import pyherc.rules.items
from random import Random
from pyherc.data import Level
from pyherc.test.builders import ItemBuilder
from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import EffectHandleBuilder
from pyherc.test.builders import ActionFactoryBuilder

from hamcrest import * #pylint: disable=W0401
from mockito import mock

class TestItems(object):
    """
    Tests for items
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestItems, self).__init__()
        self.item = None
        self.level = None
        self.dungeon = None
        self.character = None

    def setup(self):
        """
        Setup for this test case
        """
        self.item = (ItemBuilder()
                        .with_name('banana')
                        .build())

        self.level = Level([20, 20])

        self.character = (CharacterBuilder()
                            .with_action_factory(ActionFactoryBuilder()
                                                    .with_move_factory())
                            .with_level(self.level)
                            .with_location((5, 5))
                            .build())

        self.level.add_item(self.item, (5, 5))

    def test_wield_weapon(self):
        """
        Test that character can wield a weapon (dagger)
        """
        item = ItemBuilder().build()

        assert_that(item, is_not(is_in(self.character.weapons)))

        pyherc.rules.items.wield(mock(), self.character, item)

        assert_that(item, is_in(self.character.weapons))

    def test_unwielding_item(self):
        """
        Test that wielded item can be unwielded
        """
        item = ItemBuilder().build()
        pyherc.rules.items.wield(mock(), self.character, item)

        assert_that(item, is_in(self.character.weapons))

        pyherc.rules.items.unwield(mock(), self.character, item)

        assert_that(item, is_not(is_in(self.character.weapons)))

    def test_dual_wielding(self):
        """
        Test that character can wield two weapons
        """
        item1 = (ItemBuilder()
                        .with_name('dagger')
                        .with_tag('light weapon')
                        .with_damage(1)
                        .build())

        item2 = (ItemBuilder()
                        .with_name('sickle')
                        .with_tag('light weapon')
                        .with_damage(2)
                        .build())

        assert_that(item1, is_not(is_in(self.character.weapons)))
        assert_that(item2, is_not(is_in(self.character.weapons)))

        pyherc.rules.items.wield(mock(), self.character, item1)
        pyherc.rules.items.wield(mock(),
                                 self.character,
                                 item2,
                                 dual_wield = True)

        assert_that(item1, is_in(self.character.weapons))
        assert_that(item2, is_in(self.character.weapons))

    def test_dual_wielding_two_handed_weapons(self): #pylint: disable=C0103
        """
        Test that character can not dual wield two-handed weapon
        """
        item1 = (ItemBuilder()
                        .with_name('longspear')
                        .with_tag('two-handed weapon')
                        .with_tag('weapon')
                        .build())

        item2 = (ItemBuilder()
                        .with_name('sickle')
                        .with_tag('light weapon')
                        .with_tag('weapon')
                        .build())

        assert_that(item1, is_not(is_in(self.character.weapons)))
        assert_that(item2, is_not(is_in(self.character.weapons)))

        pyherc.rules.items.wield(mock(), self.character, item2)
        pyherc.rules.items.wield(mock(), self.character,
                                 item1,
                                 dual_wield = True)

        assert_that(item1, is_not(is_in(self.character.weapons)))
        assert_that(item2, is_in(self.character.weapons))

    def test_can_dual_wield(self):
        """
        Test that system can determine if two items can be dual-wielded
        """
        item1 = (ItemBuilder()
                    .with_name('longspear')
                    .with_tag('weapon')
                    .with_damage(2)
                    .build())

        item2 = (ItemBuilder()
                    .with_name('sickle')
                    .with_tag('light weapon')
                    .with_damage(1)
                    .build())

        assert(not pyherc.rules.items.can_dual_wield(
                                                     mock(),
                                                     self.character,
                                                     item1,
                                                     item2))

    def test_dual_wieldable(self):
        """
        Test that system can determine if item is dual-wieldable
        """
        item1 = (ItemBuilder()
                    .with_name('longspear')
                    .with_tag('weapon')
                    .with_damage(3)
                    .build())

        item2 = (ItemBuilder()
                    .with_name('sickle')
                    .with_tag('light weapon')
                    .with_damage(1)
                    .build())

        assert(not pyherc.rules.items.is_dual_wieldable(
                                                        mock(),
                                                        self.character,
                                                        item1))
        assert(pyherc.rules.items.is_dual_wieldable(
                                                    mock(),
                                                    self.character,
                                                    item2))

    def test_dual_wieldable_apples(self):
        """
        Test determing if item is dual-wieldable when using mundane items
        """
        item = (ItemBuilder()
                    .with_name('apple')
                    .with_tag('food')
                    .build())

        assert(not pyherc.rules.items.is_dual_wieldable(
                                                        mock(),
                                                        self.character,
                                                        item))

    def test_tags(self):
        """
        Test that different types of items have tags
        """
        item = ItemBuilder().build()

        assert(item.get_tags() is not None)

    def test_main_type_basic(self):
        """
        Test that main type can be retrieved
        """
        self.item = (ItemBuilder()
                    .with_tag('weapon')
                    .build())

        main_type = self.item.get_main_type()

        assert(main_type == 'weapon')

        self.item = (ItemBuilder()
                        .with_tag('food')
                        .build())

        main_type = self.item.get_main_type()

        assert(main_type == 'food')

class TestItemsInLevel:
    """
    Tests performed with items that are placed on levels
    """
    def __init__(self):
        """
        Default constructor
        """
        self.item = None
        self.level = None
        self.dungeon = None
        self.model = None
        self.character = None
        self.rng = None

    def setup(self):
        """
        Setup this test case
        """
        self.rng = Random()

        self.item = (ItemBuilder()
                        .build())

        self.level = Level([20, 20])

        self.character = (CharacterBuilder()
                            .with_location((5, 5))
                            .with_level(self.level)
                            .with_action_factory(
                                ActionFactoryBuilder()
                                    .with_inventory_factory())
                            .build())

        self.level.add_item(self.item, (5, 5))

        self.dungeon = pyherc.data.dungeon.Dungeon()
        self.dungeon.levels = self.level

        self.model = pyherc.data.model.Model()
        self.model.dungeon = self.dungeon
        self.model.player = self.character

    def test_picking_up(self):
        """
        Test that item can be picked up
        """
        assert(self.character.location == (5, 5))
        assert(self.item.location == (5, 5))

        self.character.pick_up(self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)
        assert(self.item.location == ())

    def test_picking_up_not_correct_location(self): #pylint: disable=C0103
        """
        Test that item is not picked up from wrong location
        """
        self.character.location = (6, 6)

        assert(self.character.location == (6, 6))
        assert(self.item.location == (5, 5))

        self.character.pick_up(self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)

    def test_dropping_item(self):
        """
        Test that an item can be dropped from inventory
        """
        self.character.pick_up(self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)

        self.character.location = (8, 8)
        pyherc.rules.items.drop(self.model, self.character, self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)
        assert(self.item.location == (8, 8))

    def test_dropping_wielded_item(self):
        """
        Test that wielded item is dropped correctly
        """
        self.character.pick_up(self.item)
        pyherc.rules.items.wield(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)
        assert(self.item in self.character.weapons)

        self.character.location = (8, 8)
        pyherc.rules.items.drop(self.model, self.character, self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)
        assert(self.item.location == (8, 8))
        assert(not self.item in self.character.weapons)

    def test_finding_items(self):
        """
        Test that level can be queried for items on a certain location
        """
        item = (ItemBuilder()
                    .with_name('apple')
                    .build())
        self.level.add_item(item, (5, 5))

        item = (ItemBuilder()
                    .with_name('kiwi')
                    .build())
        self.level.add_item(item, (3, 3))

        items = self.level.get_items_at((5, 5))
        assert(len(items) == 2)

        items = self.level.get_items_at((3, 3))
        assert(len(items) == 1)

        items = self.level.get_items_at((12, 0))
        assert(len(items) == 0)

class TestItemAdvanced():
    """
    Testing more advanced features of item class
    """
    def __init__(self):
        """
        Default constructor
        """
        self.character = None

    def setup(self):
        """
        Setup test case
        """
        self.character = (CharacterBuilder()
                            .build())

    def test_appearance_of_unknown(self):
        """"
        Test that appearance is reported for an unknown item
        """

        item = (ItemBuilder()
                    .with_name('healing potion')
                    .with_appearance('blue potion')
                    .build())

        name = item.get_name(self.character)

        assert(name == 'blue potion')

    def test_appearance_of_generic_named_item(self): #pylint: disable=C0103
        """
        Test that given name is reported for a generally named item
        """
        item = (ItemBuilder()
                    .with_name('healing potion')
                    .with_appearance('blue potion')
                    .build())

        self.character.item_memory['healing potion'] = 'doozer potion'

        name = item.get_name(self.character)

        assert_that(name, is_(equal_to('doozer potion')))

    def test_identifying_item(self):
        """
        Test that character can identify an item
        """
        item = (ItemBuilder()
                    .with_name('healing potion')
                    .with_appearance('blue potion')
                    .build())

        name = item.get_name(self.character)
        assert_that(name, is_(equal_to('blue potion')))

        self.character.identify_item(item)

        name = item.get_name(self.character)
        assert_that(name, is_(equal_to('healing potion')))

    def test_item_name_decoration(self):
        """
        Test that item can decorate its name
        """
        item = (ItemBuilder()
                    .with_name('club')
                    .build())

        self.character.inventory.append(item)
        name = item.get_name(self.character)
        assert_that(name, is_(equal_to('club')))

        self.character.weapons = [item]
        name = item.get_name(self.character, True)
        assert_that(name, is_(equal_to('club (weapon in hand)')))

        name = item.get_name(self.character, False)
        assert_that(name, is_(equal_to('club')))

class TestItemEffects:
    """
    Tests related to effects on items
    """
    def __init__(self):
        """
        Default constructor
        """
        self.item = None
        self.effect1 = None
        self.effect2 = None

    def setup(self):
        """
        Set up the test with an item and two effects
        """
        self.effect1 = (EffectHandleBuilder()
                            .with_trigger('on drink')
                            .build())
        self.effect2 = (EffectHandleBuilder()
                            .with_trigger('on break')
                            .build())
        self.item = (ItemBuilder()
                        .with_effect(self.effect1)
                        .with_effect(self.effect2)
                        .build())

    def test_get_all_effects(self):
        """
        Test that all effects can be returned
        """

        effects = self.item.get_effect_handles()

        assert(self.effect1 in effects)
        assert(self.effect2 in effects)
        assert(len(effects) == 2)

    def test_get_effects_by_trigger(self):
        """
        Test that effects triggered by certain trigger can be returned
        """

        effects = self.item.get_effect_handles('on break')
        assert(not self.effect1 in effects)
        assert(self.effect2 in effects)
        assert(len(effects) == 1)

    def test_get_nonexistent_effect(self):
        """
        Test that items without effects don't crash effects returning
        """

        handles = self.item.get_effect_handles('on hit')
        assert(handles == [])

    def test_get_multiple_effects_by_type(self): #pylint: disable=C0103
        """
        Test that multiple effects can be returned by type
        """

        effect3 = (EffectHandleBuilder()
                        .with_trigger('on break')
                        .build())
        self.item.add_effect_handle(effect3)

        effects = self.item.get_effect_handles('on break')
        assert_that(self.effect2, is_in(effects))
        assert_that(effect3, is_in(effects))
        assert_that(len(effects), is_(equal_to(2)))

class TestItemCharges:
    """
    Test charge handling of items
    """
    def __init__(self):
        """
        Default constructor
        """
        self.item = None

    def setup(self):
        """
        Set up the test with an item and two effects
        """

        self.item = (ItemBuilder()
                        .with_effect(EffectHandleBuilder()
                                .with_trigger('on drink')
                                .with_charges(1))
                        .build())

    def test_get_single_charge(self):
        """
        Test that amount of charges left can be retrieved
        """
        charges = self.item.charges_left

        assert(len(charges) == 1)
        assert(1 in charges)

    def test_multiple_charges(self):
        """
        Test that amount of charges can be retrieved with multiple effects
        """
        effect2 = (EffectHandleBuilder()
                        .with_trigger('on kick')
                        .with_effect('fire')
                        .with_charges(2)
                        .build())
        self.item.add_effect_handle(effect2)

        charges = self.item.charges_left

        assert(len(charges) == 2)
        assert(1 in charges)
        assert(2 in charges)

    def test_extremes_with_multiple_charges(self): #pylint: disable=C0103
        """
        Test that smallest and biggest amount of charges left can be retrieved
        """
        effect2 = (EffectHandleBuilder()
                        .with_trigger('on kick')
                        .with_effect('poison')
                        .with_charges(2)
                        .build())
        self.item.add_effect_handle(effect2)

        minimum_charges = self.item.minimum_charges_left
        assert(minimum_charges == 1)

        maximum_charges = self.item.maximum_charges_left
        assert(maximum_charges == 2)
