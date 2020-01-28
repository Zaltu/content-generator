"""
Sequential random content generation factory.
"""
#pylint: disable=attribute-defined-outside-init
from faker import Faker
from faker.factory import Factory

class Fuker(Faker):
    """
    Wrapper to generate the feature sequence surrounding whatever content is asked for.
    """
    faker = Faker()

    def setLocale(self, *args):
        """
        Give faker the option of not being completely useless and allowing each instance to change locales on
        demand.

        :param args: new desired locale(s)
        """
        locales = list(args)
        self._factory_map = {}
        for locale in locales:
            self._factory_map[locale] = Factory.create(locale, None, None, None)
        self._locales = locales
        self._factories = list(self._factory_map.values())
