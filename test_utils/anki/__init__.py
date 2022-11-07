from typing import List
from typing import Optional
import sys

from unittest.mock import MagicMock

class MockAnkiModules:
    """
    I'd like to get rid of the situation when this is required, but for now this helps with the situation that
    anki modules are not available during test runtime.
    """
    module_names_list = ['anki', 'anki.hooks', 'anki.exporting', 'anki.decks', 'anki.utils', 'anki.cards', 'anki.models',
                         'anki.notes', 'aqt', 'aqt.qt', 'aqt.exporting', 'aqt.utils']

    def __init__(self, module_names_list: Optional[List[str]] = None):
        if module_names_list is None:
            module_names_list = self.module_names_list

        self.shadowed_modules = {}

        for module_name in module_names_list:
            self.shadowed_modules[module_name] = sys.modules.get(module_name)
            sys.modules[module_name] = MagicMock()

    def unmock(self):
        for module_name, module in self.shadowed_modules.items():
            if module is not None:
                sys.modules[module_name] = module
            else:
                if module_name in sys.modules:
                    del sys.modules[module_name]
