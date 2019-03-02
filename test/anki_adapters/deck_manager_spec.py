from expects import expect, contain_only
from mamba import description, it, before
from typing import Iterable
from unittest.mock import MagicMock

from crowd_anki.anki_adapters.anki_deck import AnkiDeck
from crowd_anki.anki_adapters.deck_manager import AnkiStaticDeckManager

dynamic_deck = AnkiDeck({'dyn': True})
static_deck = AnkiDeck({'dyn': False})

internal_deck_names = ['a1::a2', 'b1', 'd1', 'a1']
override_deck_names = ['a1::a2', 'b1']
non_overridden_decks = ['c1', 'd1::d2']
leaf_deck_names = ['a1::a2::a3', 'b1::b2'] + non_overridden_decks


def deck_for_name(name):
    return AnkiDeck({'name': name, 'dyn': False})


def dummy_deck_for_names(names):
    return [deck_for_name(name) for name in names]


def data_from_decks(decks: Iterable[AnkiDeck]):
    return [deck.data for deck in decks]


internal_decks = dummy_deck_for_names(internal_deck_names)
leaf_decks = dummy_deck_for_names(leaf_deck_names)
override_decks = dummy_deck_for_names(override_deck_names)

with description(AnkiStaticDeckManager) as self:
    def mock_internal_manager(self, decks):
        self.internal_manager.all.return_value = data_from_decks(decks)


    with before.each:
        self.internal_manager = MagicMock()
        self.static_deck_manager = AnkiStaticDeckManager(self.internal_manager)
        self.mock_internal_manager(internal_decks + leaf_decks)

    with it('filters out dynamic decks, when you ask for all'):
        self.mock_internal_manager([dynamic_deck, static_deck])
        expect(self.static_deck_manager.all()).to(contain_only(static_deck))

    with it('returns only decks without children, when asked for leaf_decks'):
        expect(self.static_deck_manager.leaf_decks()).to(contain_only(*leaf_decks))

    with it('when overrides are supplied - it returns them as leaf nodes, and does not return their children'):
        expect(self.static_deck_manager.leaf_decks(override_decks)) \
            .to(contain_only(*(override_decks + dummy_deck_for_names(non_overridden_decks))))

    with it('ignores non-existent overrides'):
        expect(self.static_deck_manager.leaf_decks(override_decks + [deck_for_name('non_existent_deck')])) \
            .to(contain_only(*(override_decks + dummy_deck_for_names(non_overridden_decks))))
