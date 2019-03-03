from abc import ABC, abstractmethod

from dataclasses import dataclass
from functional import seq
from pygtrie import StringTrie
from typing import Iterable, Any

from ..adapters.anki_deck import AnkiDeck
from ...utils.trie import keys_without_children
from ...utils.trie import remove_children_of


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
        return seq(self.internal_deck_manager.all()) \
            .map(lambda d: AnkiDeck(d)) \
            .filter(lambda d: not d.is_dynamic) \
            .to_list()

    def leaf_decks(self, overrides: Iterable[AnkiDeck] = tuple()) -> Iterable[AnkiDeck]:
        deck_trie = self.deck_trie()
        override_keys = [deck.name for deck in overrides]

        remove_children_of(deck_trie, override_keys)
        keys = keys_without_children(deck_trie)

        return [deck_trie[key] for key in keys]

    def deck_trie(self):
        return StringTrie(**self.decks_by_name(), separator=AnkiDeck.deck_name_separator)
