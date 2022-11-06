import sys

from unittest.mock import MagicMock

class MockAnkiModules:
    """
    I'd like to get rid of the situation when this is required, but for now this helps with the situation that
    anki modules are not available during test runtime.
    """
    modules_list = ['anki', 'anki.hooks', 'anki.exporting', 'anki.decks', 'anki.utils', 'anki.cards', 'anki.models',
                    'anki.notes', 'aqt', 'aqt.qt', 'aqt.exporting', 'aqt.utils']

    def __init__(self):
        self.shadowed_modules = {}

        for module in self.modules_list:
            self.shadowed_modules[module] = sys.modules.get(module)
            sys.modules[module] = MagicMock()

    def unmock(self):
        for module in self.modules_list:
            shadowed_module = self.shadowed_modules[module]
            if shadowed_module is not None:
                sys.modules[module] = shadowed_module
            else:
                if module in sys.modules:
                    del sys.modules[module]
