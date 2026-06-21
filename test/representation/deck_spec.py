from mamba import description, it
from expects import expect, equal

from crowd_anki.representation.deck import Deck


def _make_deck(notes=0, media_files=None, children=None):
    deck = Deck(file_provider_supplier=None)
    deck.notes = [None] * notes
    deck.media_files = list(media_files or [])
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
            expect(_make_deck(media_files=['a.jpg', 'b.jpg', 'c.jpg']).get_media_file_count()).to(equal(3))

        with it("counts media files recursively across subdecks"):
            deck = _make_deck(media_files=['a.jpg'], children=[
                _make_deck(media_files=['b.jpg', 'c.jpg'], children=[
                    _make_deck(media_files=['d.jpg', 'e.jpg', 'f.jpg']),
                ]),
            ])
            expect(deck.get_media_file_count()).to(equal(6))

        with it("counts media files in subdecks even when the parent has none"):
            deck = _make_deck(children=[_make_deck(media_files=['a.jpg', 'b.jpg', 'c.jpg', 'd.jpg'])])
            expect(deck.get_media_file_count()).to(equal(4))

        with it("counts media files shared across subdecks only once"):
            deck = _make_deck(media_files=['shared.jpg'], children=[
                _make_deck(media_files=['shared.jpg', 'a.jpg']),
                _make_deck(media_files=['shared.jpg', 'b.jpg']),
            ])
            expect(deck.get_media_file_count()).to(equal(3))

        with it("counts media files duplicated within a single deck only once"):
            expect(_make_deck(media_files=['a.jpg', 'a.jpg']).get_media_file_count()).to(equal(1))
