from expects import expect, be, equal
from mamba import description, it
from unittest.mock import MagicMock

from crowd_anki.representation import deck_initializer

DYNAMIC_DECK = {'dyn': True}

TEST_DECK = "test deck"


def _deck_json(media_files=None, children=None):
    return {
        "deck_config_uuid": "config-uuid",
        "notes": [],
        "media_files": media_files or [],
        "children": children or [],
    }


with description("Initializer from deck") as self:
    with it("should return None when trying to export dynamic deck"):
        collection = MagicMock()

        collection.decks.byName.return_value = DYNAMIC_DECK

        expect(deck_initializer.from_collection(collection, TEST_DECK)).to(be(None))

    with description("from_json") as self:
        with it("populates media_files from JSON, including subdecks"):
            json_dict = _deck_json(
                media_files=["a.png", "b.png"],
                children=[_deck_json(media_files=["c.png"])],
            )

            deck = deck_initializer.from_json(json_dict)

            expect(deck.get_media_file_count()).to(equal(3))
