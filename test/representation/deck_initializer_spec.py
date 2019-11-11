from expects import expect, be
from mamba import description, it
from unittest.mock import MagicMock

from crowd_anki.representation import deck_initializer

DYNAMIC_DECK = {'dyn': True}

TEST_DECK = "test deck"

TEST_CONFIG = MagicMock()

with description("Initializer from deck") as self:
    with it("should return None when trying to export dynamic deck"):
        collection = MagicMock()

        collection.decks.byName.return_value = DYNAMIC_DECK

        expect(deck_initializer.from_collection(collection, TEST_CONFIG, TEST_DECK)).to(be(None))
