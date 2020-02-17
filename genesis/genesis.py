"""
Generate all kinds of data for any use.
This is a central regrouping place to grab and expose the best parts of multiple content generators for the
ultimate content experience.
"""
#pylint: disable=no-self-use
from faker import Faker
import lorem

import DDChar

class Genesis:
    """
    In the beginning there was the word, and the word was God, and the word is God.

    :param bool include_ai: Set to true to include the GPT2 text AI module in genesis. This requires lots of
    RAM. For more requirement information, see the ReadMe.
    """
    __dummy_faker = Faker()
    ai = None
    def __init__(self, include_ai=False):
        if include_ai:
            import AIText  # Grab some popcorn and get comfy
            self.ai = AIText

    def __getattr__(self, attr):
        """
        Distribute incoming requests to whatever module is the right one for servicing them.

        :param str attr: the attribute requested

        :returns: the correct module's implementation of the requested attribute
        :rtype: object
        """
        if attr == "text" and self.ai:
            return self.ai.speak

        if hasattr(self.__dummy_faker, attr):
            def _wrapper(locale="en_US"):
                """
                Wrap the creation of a faker instance so we can generate the correct locale.
                This is awful, terrible and deplorable, but there's no other way because of the way Faker is
                designed.

                :param str locale: locale to generate for, defaults to en_US

                :returns: wrapper function
                :rtype: function
                """
                lf = Faker(locale)
                return lf.__getattr__(attr)()
            return _wrapper

        return self.__getattribute__(attr)

    def latin(self):
        """
        Return some very cultured latin speak.

        :returns: random latin text
        :rtype: str
        """
        return lorem.text()

    def dndchar(self, **kwargs):
        """
        Get a D&D character

        :param kwargs: any user input parameters

        :returns: path to a randomly generate D&D character sheet
        :rtype: str
        """
        return DDChar.generate_dnd_character(**kwargs)
