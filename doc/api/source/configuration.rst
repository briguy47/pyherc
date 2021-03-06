Configuration
*************
Configuration of pyherc is driven by external files and internal scripts.
External files are located in resources directory and internal scripts
in package :py:mod:`pyherc.config`.

Configuration scripts
=====================
pyherc supports dynamic detection of configuration scripts. The system can be
configured by placing all scripts containing configuration in a single 
package and supplying that package to :class:`pyherc.config.config.Config`
class during system start:

.. code-block:: python

   self.config = Configuration(self.base_path, self.world)
   self.config.initialise(herculeum.config.levels)

Level configuration
===================
The file containing level configuration should contain following function to
perform configuration.

.. code-block:: python

    def init_level(rng, item_generator, creature_generator, level_size)

This function should create :py:class:`pyherc.generators.level.config.LevelGeneratorFactoryConfig`
with appropriate values and return it. This configuration is eventually fed to
:class:`pyherc.generators.level.generator.LevelGeneratorFactory` when new level
is requested.

Item configuration
==================
The file containing item configuration should contain following function to
perform configuration

.. code-block:: python

    def init_items():
    
This function should return a list of :class:`pyherc.generators.item.ItemConfiguration`
objects.

Character configuration
=======================
The file containing character configuration should contain following function
to perform configuration:

.. code-block:: python

   def init_creatures():
   
This function should return a list of :class:`pyherc.generators.creature.CreatureConfiguration`
objects.

Effects configuration
=====================
The file containing effects configuration should contain following function to
perform configuration

.. code-block:: python

    def init_effects():
    
This function should return a list of effect specifications.

