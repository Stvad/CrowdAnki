from abc import ABC, abstractmethod

from dataclasses import dataclass
from pygtrie import StringTrie
from typing import Iterable, Any

from ..anki_adapters.anki_deck import AnkiDeck
from ..utils.trie import keys_without_children


class DeckManager(ABC):
    @abstractmethod
    def all(self) -> Iterable[AnkiDeck]:
        pass

    @abstractmethod
    def leaf_decks(self, overrides: Iterable[AnkiDeck] = tuple()) -> Iterable[AnkiDeck]:
        pass

    def decks_by_name(self):
        return {deck.name: deck for deck in self.all()}


@dataclass
class AnkiStaticDeckManager(DeckManager):
    internal_deck_manager: Any

    def all(self) -> Iterable[AnkiDeck]:
        return [deck for deck in self.internal_deck_manager.all() if not deck.is_dynamic]

    def leaf_decks(self, overrides: Iterable[AnkiDeck] = tuple()) -> Iterable[AnkiDeck]:
        deck_trie = self.deck_trie()
        keys = keys_without_children(deck_trie)
        return [deck_trie[key] for key in keys]

    def deck_trie(self):
        return StringTrie(**self.decks_by_name(), separator=AnkiDeck.deck_name_separator)
