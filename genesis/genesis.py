"""
Generate all kinds of data for any use.
This is a central regrouping place to grab and expose the best parts of multiple content generators for the
ultimate content experience.
"""
from fuker import Fuker

class Genesis:
    """
    In the beginning there was the word, and the word was God, and the word is God.

    :param bool include_ai: Set to true to include the GPT2 text AI module in genesis. This requires lots of
    RAM. For more requirement information, see the ReadMe.
    """
    fuker = Fuker()
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
        if getattr(self.fuker, attr, None):
            return getattr(self.fuker, attr)
        return self.__getattribute__(attr)
