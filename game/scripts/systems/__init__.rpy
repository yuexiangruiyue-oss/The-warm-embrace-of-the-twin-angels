# game/scripts/systems/__init__.rpy -- System Initialization Entry
# The Embrace of the Twin Angels
# This file ensures systems load in correct init priority order.
# Ren'Py init priority: lower numbers load first.
# constants.rpy (init 0) -> state.rpy (init 1) -> systems (init 2+)

# This file intentionally left minimal.
# System modules are loaded via their own init python blocks.
