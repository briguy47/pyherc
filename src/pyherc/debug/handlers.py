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
Module for page handlers
"""
import pyherc.debug.data
from pyherc.application import APP
from web import form

web_loaded = False

try:
    import web
    web_loaded = True
except ImportError:
    web_loaded = False

def initialise_server():
    """
    Initialise render component for server
    """
    pyherc.debug.data.render = web.template.render(
                                '{0}/html/'.format(APP.base_path))

def get_urls():
    """
    Get mapping between urls and handlers

    Returns:
        Mapping that can be passed on web.application
    """
    return (
            '/', 'Index',
            '/map', 'Map',
            '/player', 'Player',
            '/factory', 'Factory'
            )

def get_debug_server():
    """
    Set up debug server

    Returns:
        Initialised debug server
    """
    if web_loaded == False:
        return None

    initialise_server()
    app = web.application(get_urls(), vars(pyherc.debug.handlers))
    return app

class Index:
    """
    Class for displaying start page
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def GET(self):
        """
        Handle http get
        """
        return pyherc.debug.data.render.index()

class Map:
    """
    Class for displaying map
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def GET(self):
        """
        Handle http get
        """
        return APP.world.player.level.dump_string()

class Player:
    """
    Class for displaying player
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def GET(self):
        """
        Handle http get
        """
        return pyherc.debug.data.render.player(APP.world.player)

class Factory:
    """
    Class for creating new objects
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def get_form(self):
        """
        Creates form to display

        Returns:
            Form
        """
        display_form = form.Form(
            form.Textbox("creature_name", description="Creature")
            )

        return display_form

    def GET(self):
        """
        Handle http get
        """
        return pyherc.debug.data.render.factory(self.get_form())

    def POST(self):
        """
        Handle http post
        """
        form_data = web.input()
        creature_name = form_data.creature_name

        creature = APP.creature_generator.generate_creature({'name':creature_name})
        player_character = APP.world.player
        level = player_character.level
        location = player_character.location

        level.add_creature(creature, (location[0] + 2, location[1]))

        return 'Created monster called {0}'.format(form_data.creature_name)
