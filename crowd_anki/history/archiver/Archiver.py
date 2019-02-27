from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Callable, Iterable

from ...anki_adapters.deck_manager import DeckManager


class Archiver(ABC):
    @abstractmethod
    def archive(self, decks: Iterable = tuple()):
        pass


@dataclass
class AllDeckArchiver(Archiver):
    decks: DeckManager
    deck_archiver_supplier: Callable[[str], Archiver]

    def archive(self, overrides: Iterable = tuple()):
        for deck in self.decks.leaf_decks(overrides):
            self.deck_archiver_supplier(deck).archive()
