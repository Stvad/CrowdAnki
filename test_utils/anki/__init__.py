import sys

from unittest.mock import MagicMock


def mock_anki_modules():
    """
    I'd like to get rid of the situation when this is required, but for now this helps with the situation that
    anki modules are not available during test runtime.
    """

    modules_list = ['anki', 'anki.hooks', 'anki.exporting', 'anki.decks', 'anki.utils', 'anki.cards', 'anki.models',
                    'anki.notes', 'aqt''', 'aqt.qt', 'aqt.exporting', 'aqt.utils']

    for module in modules_list:
        sys.modules[module] = MagicMock()
