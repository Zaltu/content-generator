"""
Module to generate random D&D characters.
"""
import os
import random
import aigis

import fantasyName

DEFAULT_PLAYER_NAME = "Dungeon Master"
DEFAULT_SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", "tmp"))

def _generate_initial_data(player=None, level=None):
    """
    Generate the data used to auto-generate a D&D character.

    :param str player: human player, defaults to the DM
    :param int level: starting level, defaults to 1

    :returns: stats required to build a character
    :rtype: dict
    """
    stats = {
        "name": fantasyName.generate(),
        "player_name": player or DEFAULT_PLAYER_NAME,
        "alignment": random.sample(aigis.dnd.ALIGNMENTS, 1)[0],
        "level": level or 1,
        "race": random.sample(aigis.dnd.RACES, 1)[0],
        "dndclass": random.sample(aigis.dnd.CLASSES, 1)[0]
    }
    # Generate subclass if above level 3
    if stats["level"] > 2:
        stats["subclass"] = random.sample(aigis.dnd.SUBCLASSES[stats["dndclass"]], 1)[0]
    # Level 1 HP
    stats["hp_max"] = aigis.dnd.CLASS_HP[stats["dndclass"]]
    # Level x HP
    stats["hp_max"] += sum(aigis.dnd.xdy(stats["level"]-1, aigis.dnd.CLASS_HP[stats["dndclass"]]))

    return stats


def generate_dnd_character(player=None, level=None):
    """
    Generate a D&D character sheet.

    :param str player: human player, defaults to the DM
    :param int level: starting level, defaults to 1

    :returns: path on disk to the generated character sheet
    :rtype: str
    """
    stats = _generate_initial_data(player, level)

    # TODO depending on class, generate chosen spells, etc...

    paths = aigis.dnd.create_character_sheet(stats)
    try:
        # Try and delete the .FDF, we don't care about it
        os.remove(paths[1])
    except (OSError, FileNotFoundError):
        # The FDF doesnt seem to exist, does the PDF?
        assert os.path.exists(paths[0])
    return paths[0]
