from expects import expect, contain_only
from mamba import description, it, before
from unittest.mock import MagicMock

from crowd_anki.anki_adapters.anki_deck import AnkiDeck
from crowd_anki.anki_adapters.deck_manager import AnkiStaticDeckManager

dynamic_deck = AnkiDeck({'dyn': True})
static_deck = AnkiDeck({'dyn': False})

internal_deck_names = ['a1::a2', 'b1']
leaf_deck_names = ['a1::a2::a3', 'b1::b2', 'c1']


def dummy_deck_for_name(name):
    return AnkiDeck({'name': name, 'dyn': False})


def dummy_deck_for_names(names):
    return [dummy_deck_for_name(name) for name in names]


internal_decks = dummy_deck_for_names(internal_deck_names)
leaf_decks = dummy_deck_for_names(leaf_deck_names)

with description(AnkiStaticDeckManager) as self:
    with before.each:
        self.internal_manager = MagicMock()
        self.static_deck_manager = AnkiStaticDeckManager(self.internal_manager)

    with it('filters out dynamic decks, when you ask for all'):
        self.internal_manager.all.return_value = [dynamic_deck, static_deck]
        expect(self.static_deck_manager.all()).to(contain_only(static_deck))

    with it('returns only decks without children, when asked for leaf_decks'):
        self.internal_manager.all.return_value = internal_decks + leaf_decks
        expect(self.static_deck_manager.leaf_decks()).to(contain_only(*leaf_decks))

    with it('when overrides are supplied - it returns them as leaf nodes, and does not return their children'):
        self.internal_manager.all.return_value = internal_decks + leaf_decks
        expect(self.static_deck_manager.leaf_decks()).to(contain_only(*leaf_decks))

    with it('ignores non-existent overrides'):
        pass
