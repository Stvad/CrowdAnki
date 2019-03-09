from cached_property import cached_property

from dataclasses import dataclass
from typing import Callable


@dataclass
class AnkiDeck:
    _data: dict

    deck_name_separator = '::'

    @property
    def data(self):
        return self._data

    @property
    def is_dynamic(self):
        return bool(self.data['dyn'])

    @property
    def name(self):
        return self.data['name']


class LazyDeck(AnkiDeck):
    def __init__(self, deck_initializer: Callable[[], dict]):
        self.deck_initializer = deck_initializer

    @cached_property
    def data(self):
        return self.deck_initializer()


class NamedLazyDeck(LazyDeck):
    def __init__(self, name: str, name_initializer: Callable[[str], dict]):
        super().__init__(lambda: name_initializer(name))
        self._name = name

    @property
    def name(self):
        return self._name
