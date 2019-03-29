from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Callable, Iterable

from ..anki.adapters.anki_deck import AnkiDeck
from ..anki.adapters.deck_manager import DeckManager


class Archiver(ABC):
    @abstractmethod
    def archive(self, decks: Iterable = tuple(), reason: str = None):
        pass


@dataclass
class AllDeckArchiver(Archiver):
    decks: DeckManager
    deck_archiver_supplier: Callable[[AnkiDeck], Archiver]

    def archive(self, overrides: Iterable = tuple(), reason: str = None):
        for deck in self.decks.leaf_decks(overrides):  # todo asyncio?
            self.deck_archiver_supplier(deck).archive(reason=reason)
