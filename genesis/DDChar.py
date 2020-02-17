"""
Module to generate random D&D characters.
"""
import os
import random
import aigis

import fantasyName

DEFAULT_PLAYER_NAME = "Dungeon Master"
DEFAULT_SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))

CHAR_ATTR_NAMES = {"strength", "dexterity", "intelligence", "wisdom", "constitution", "charisma"}

def _generate_initial_data(**kwargs):
    """
    Generate the data used to auto-generate a D&D character.

    :param kwargs: any user input parameters

    :returns: stats required to build a character
    :rtype: dict
    """
    stats = {
        "name": kwargs.get("name") or fantasyName.generate(),
        "player_name": kwargs.get("player") or DEFAULT_PLAYER_NAME,
        "alignment": kwargs.get("alignment") or random.sample(aigis.dnd.ALIGNMENTS, 1)[0],
        "level": kwargs.get("level") or 1,
        "race": kwargs.get("race") or random.sample(aigis.dnd.RACES, 1)[0],
        "class": kwargs.get("class") or random.sample(aigis.dnd.CLASSES, 1)[0]
    }
    # Generate subclass if above level 3
    if stats["level"] > 2:
        stats["subclass"] = kwargs.get("subclass") or \
                            random.sample(aigis.dnd.SUBCLASSES[stats["class"]], 1)[0]
    # Level 1 HP
    stats["hp_max"] = aigis.dnd.CLASS_HP[stats["class"]]
    # Level x HP
    stats["hp_max"] += sum(aigis.dnd.xdy(aigis.dnd.CLASS_HP[stats["class"]], stats["level"]-1))

    return stats


def _generate_random_stats():
    """
    Generate 7x(4d6-lowest)-lowest

    :returns: 6x(4d6-lowest)
    :rtype: list
    """
    vals = []
    for _ in range(0, 7):
        rolls = aigis.dnd.xdy(6, 4)
        rolls.sort()
        rolls = rolls[1:]
        vals.append(sum(rolls))
    vals.sort()
    if sum(vals[1:]) < 10:
        return _generate_random_stats()
    return vals[1:]


def _generate_attr_values():
    """
    Generate values for the character's attributes (Str, Dex, etc...)
    Uses 7x(4d6-lowest)-lowest and random assignation.

    :returns: stats
    :rtype: dict
    """
    vals = _generate_random_stats()
    stats = {}
    for attr in CHAR_ATTR_NAMES:
        stats[attr] = vals.pop(random.randint(0, len(vals)-1))
    return stats



def generate_dnd_character(**kwargs):
    """
    Generate a D&D character sheet.

    :param kwargs: any user input parameters

    :returns: path on disk to the generated character sheet
    :rtype: str
    """
    stats = _generate_initial_data(**kwargs)
    stats.update(_generate_attr_values())

    # TODO depending on class, generate chosen spells, etc...

    paths = aigis.dnd.create_character_sheet(DEFAULT_SAVE_PATH, **stats)
    try:
        # Try and delete the .FDF, we don't care about it
        os.remove(paths[1])
    except (OSError, FileNotFoundError):
        # The FDF doesnt seem to exist, does the PDF?
        assert os.path.exists(paths[0])
    return paths[0]
