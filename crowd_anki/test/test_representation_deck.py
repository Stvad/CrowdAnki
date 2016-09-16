import unittest

from crowd_anki.representation.deck import Deck


class DeckRepresentationTest(unittest.TestCase):
    def setUp(self):
        self.tdeck = Deck()

    def test_notecount_empty(self):
        self.assertEqual(self.tdeck.get_note_count(), 0)

    def test_notecount_no_notes(self):
        self.tdeck.children.append(Deck())
        self.tdeck.children[0].notes.append(1)

        self.assertEqual(self.tdeck.get_note_count(), 1)

