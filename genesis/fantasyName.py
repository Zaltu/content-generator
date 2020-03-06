"""
Generate a fantasy-world sounding name.
"""
import random

FIRST_NAMES = [
    "Tordrick", "Alovar", "Sorel", "Urok", "Kerrilian", "Kruber", "Lian", "Bardin", "Lyra", "Eleanor",
    "Reginald", "Belethor", "Malakay", "Devan", "Nayeli", "Derrill", "Irvin", "Ollivander", "Keegan",
    "Ulrich", "Gelendale", "Haley", "Festus", "Fenrir", "Marick", "Aurora", "Trea", "Bayela", "Aayla",
]
LAST_NAMES = [
    "Saltspyer", "Kibbler", "Ostanta", "Thiel", "Grimes", "Oyvind", "Bijin", "Secura",
]
NAME_CHUNKS = [
    "fire", "wind", "hammer", "bright", "stone", "stalker", "tree", "trick", "foot", "arms", "steady",
    "bearer", "torch", "silk", "weaver", "smooth", "tongue", "beast", "brave", "heart", "forge", "wild",
    "dark", "walker", "sharp", "quick", "high", "rod",
]

def generate(composed=False):
    """
    Generate a fanstay-sounding name using some generic templates.

    :param bool composed: whether to force a 2-part last name, default-false

    :returns: first name, last name
    :rtype: str
    """
    firstname = random.sample(FIRST_NAMES, 1)[0]
    if composed or random.randint(1, 2) == 1:
        lastname = random.sample(NAME_CHUNKS, 1)[0]
        lastname2 = random.sample(NAME_CHUNKS, 1)[0]
        while lastname2 == lastname:
            lastname2 = random.sample(NAME_CHUNKS, 1)[0]
        lastname += lastname2
        lastname = lastname.capitalize()
    else:
        lastname = random.sample(LAST_NAMES, 1)[0]
    return " ".join([firstname, lastname])


if __name__ == "__main__":
    print(generate())
