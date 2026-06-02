from mamba import description, it
from expects import expect, equal

from crowd_anki.representation.deck import Deck


def _make_deck(notes=0, media_files=0, children=None):
    deck = Deck(file_provider_supplier=None)
    deck.notes = [None] * notes
    deck.media_files = ['file'] * media_files
    deck.children = children or []
    return deck


with description(Deck) as self:
    with description(".get_note_count") as self:
        with it("returns 0 for an empty deck"):
            expect(_make_deck().get_note_count()).to(equal(0))

        with it("counts notes in a flat deck"):
            expect(_make_deck(notes=3).get_note_count()).to(equal(3))

        with it("counts notes recursively across subdecks"):
            deck = _make_deck(notes=1, children=[
                _make_deck(notes=2, children=[
                    _make_deck(notes=3),
                ]),
            ])
            expect(deck.get_note_count()).to(equal(6))

        with it("counts notes in subdecks even when the parent has none"):
            deck = _make_deck(notes=0, children=[_make_deck(notes=5)])
            expect(deck.get_note_count()).to(equal(5))

    with description(".get_media_file_count") as self:
        with it("returns 0 for an empty deck"):
            expect(_make_deck().get_media_file_count()).to(equal(0))

        with it("counts media files in a flat deck"):
            expect(_make_deck(media_files=3).get_media_file_count()).to(equal(3))

        with it("counts media files recursively across subdecks"):
            deck = _make_deck(media_files=1, children=[
                _make_deck(media_files=2, children=[
                    _make_deck(media_files=3),
                ]),
            ])
            expect(deck.get_media_file_count()).to(equal(6))

        with it("counts media files in subdecks even when the parent has none"):
            deck = _make_deck(media_files=0, children=[_make_deck(media_files=4)])
            expect(deck.get_media_file_count()).to(equal(4))
