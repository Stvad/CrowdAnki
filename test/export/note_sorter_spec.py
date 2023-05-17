import logging
from random import shuffle
from unittest.mock import MagicMock

# # TODO? Stop mocking (See blame commit message and possibly PR for
# # discussion.)
# from aqt import mw
mw = MagicMock()

from mamba import describe, it, context

from crowd_anki.config.config_settings import ConfigSettings, NoteSortingMethods
from crowd_anki.export.note_sorter import NoteSorter
from crowd_anki.representation.deck import Deck
from crowd_anki.anki.adapters.note_model_file_provider import NoteModelFileProvider

test_guids = ["abc", "bcd", "cde", "def", "efg", "fgh"]
test_flags = [0, 1, 2, 3, 4, 5]
test_tags = ["adjectives", "directions", "interesting", "nouns", "verbs", "zzzzFinal"]
test_notemodels = ["Default", "LL Noun", "LL Sentence", "LL Verb", "LL Word", "Zulu"]
test_notemodelids = test_guids
test_fields = test_tags

note_sorting_single_result_pairs = [
    (NoteSortingMethods.GUID, test_guids),
    (NoteSortingMethods.FLAG, test_flags),
    (NoteSortingMethods.TAG, test_tags),
    (NoteSortingMethods.NOTE_MODEL_NAME, test_notemodels),
    (NoteSortingMethods.NOTE_MODEL_ID, test_notemodelids),
    (NoteSortingMethods.FIELD1, test_fields),
    (NoteSortingMethods.FIELD2, test_fields)
]

test_multikey_notemodel_guid = [(notemodel, guid) for notemodel in test_notemodels for guid in test_guids]

class NoteSorterTester:
    def __init__(self):
        self.note_sorter = None
        self.notes = []
        self.sorted_notes = []

        self.config = ConfigSettings(mw.addonManager, None, mw.pm)

    @staticmethod
    def get_single_note_mock(i):
        note = MagicMock()

        note.anki_object.guid = test_guids[i]
        note.anki_object.flags = test_flags[i]
        note.anki_object.tags = test_tags[i]

        note.anki_object._model = {
            "name": test_notemodels[i],
            "crowdanki_uuid": test_notemodelids[i]
        }

        note.anki_object.fields = [test_fields[i], test_fields[i]]

        return note

    @staticmethod
    def get_multikey_note_mock(i):
        note = MagicMock()

        note.anki_object.guid = test_multikey_notemodel_guid[i][1]

        note.anki_object._model = {
            "name": test_multikey_notemodel_guid[i][0]
        }

        return note

    @classmethod
    def get_notes_mock(cls, is_multi_key: bool):
        random_range = list(range(0, len(test_multikey_notemodel_guid if is_multi_key else test_guids)))
        shuffle(random_range)

        if is_multi_key:
            notes_list = [cls.get_multikey_note_mock(i) for i in random_range]
        else:
            notes_list = [cls.get_single_note_mock(i) for i in random_range]

        logging.info("Shuffled list: ", notes_list)
        return notes_list

    def setup_notes(self, is_multi_key: bool):
        self.notes = self.get_notes_mock(is_multi_key)

    def sort_with(self, sort_methods, reverse_sort, is_multi_key=False):
        self.setup_notes(is_multi_key)

        self.config.export_note_sort_methods = sort_methods
        self.config.export_notes_reverse_order = reverse_sort
        self.note_sorter = NoteSorter(self.config)
        self.sorted_notes = self.note_sorter.sort_notes(self.notes)


with describe(NoteSorterTester) as self:
    with context("user sorts by each sort option"):
        with it("do not sort / sort by none"):
            self.tester = NoteSorterTester()
            self.tester.sort_with([NoteSortingMethods.NO_SORTING.value], False)

            assert (self.tester.sorted_notes == self.tester.notes)

        with it("do not sort / sort by none, reversed"):
            self.tester = NoteSorterTester()
            self.tester.sort_with([NoteSortingMethods.NO_SORTING.value], True)

            assert (self.tester.sorted_notes == list(reversed(self.tester.notes)))

        with it("sorts by all sorting methods"):
            for method, result in note_sorting_single_result_pairs:
                self.tester = NoteSorterTester()

                self.tester.sort_with([method], False)

                assert ([NoteSorter.sorting_definitions[method](note) for note in self.tester.sorted_notes] == result)

        with it("sorts by all single sorting methods, reversed"):
            for method, result in note_sorting_single_result_pairs:
                self.tester = NoteSorterTester()

                self.tester.sort_with([method], True)

                assert ([NoteSorter.sorting_definitions[method](note) for note in self.tester.sorted_notes
                         ] == list(reversed(result)))

        with it("sorts by two sorting methods, notemodels+guids"):
            self.tester = NoteSorterTester()

            self.tester.sort_with([NoteSortingMethods.NOTE_MODEL_NAME, NoteSortingMethods.GUID], False,
                                  is_multi_key=True)

            return_object = [
                (NoteSorter.sorting_definitions[NoteSortingMethods.NOTE_MODEL_NAME](note),
                 NoteSorter.sorting_definitions[NoteSortingMethods.GUID](note))
                for note in self.tester.sorted_notes
            ]

            assert (return_object == test_multikey_notemodel_guid)

        with it("sorts by two sorting methods, notemodels+guids, reversed"):
            self.tester = NoteSorterTester()

            self.tester.sort_with([NoteSortingMethods.NOTE_MODEL_NAME, NoteSortingMethods.GUID], True,
                                  is_multi_key=True)

            return_object = [
                (NoteSorter.sorting_definitions[NoteSortingMethods.NOTE_MODEL_NAME](note),
                 NoteSorter.sorting_definitions[NoteSortingMethods.GUID](note))
                for note in self.tester.sorted_notes
            ]

            assert (return_object == list(reversed(test_multikey_notemodel_guid)))

class DeckSorterTester:
    def __init__(self):
        self.config = ConfigSettings(mw.addonManager, None, mw.pm)
        self.note_sorter = None

    def setup_note_sorter(self, sort_methods, reverse_sort):
        self.config.export_note_sort_methods = sort_methods
        self.config.export_notes_reverse_order = reverse_sort
        self.note_sorter = NoteSorter(self.config)

    @staticmethod
    def create_deck_with_subdecks(notes=None, subdecks=None):
        """Helper function to create a deck with subdecks.

        Notes and subdecks are lists of notes and decks, respectively.
        Either can be empty.

        """
        if notes is None:
            notes = []
        if subdecks is None:
            subdecks = []

        deck = Deck(NoteModelFileProvider)
        deck.notes = notes
        deck.children = subdecks
        return deck

    @classmethod
    def create_deck_with_random_notes(cls, is_multi_key: bool = False):
        return cls.create_deck_with_subdecks(
            NoteSorterTester.get_notes_mock(is_multi_key)
        )

with describe(DeckSorterTester) as self:
    with context("user sorts by each sort option"):
        with it("sorts recursively through subdecks"):
            for method, _ in note_sorting_single_result_pairs:
                self.tester = DeckSorterTester()

                # Create decks with notes
                deck1 = self.tester.create_deck_with_random_notes()
                deck2 = self.tester.create_deck_with_random_notes()
                deck3 = self.tester.create_deck_with_random_notes()

                # Create main deck with subdecks
                main_deck = self.tester.create_deck_with_subdecks([], [deck1, deck2, deck3])

                self.tester.config.export_note_sort_methods = [method]
                self.tester.config.export_notes_reverse_order = False
                self.tester.setup_note_sorter([method], False)
                self.tester.note_sorter.sort_deck(main_deck)

                # Check that notes in main deck and all subdecks are sorted
                assert (sorted(main_deck.notes, key=NoteSorter.sorting_definitions[method]) == main_deck.notes)
                for subdeck in main_deck.children:
                    assert (sorted(subdeck.notes, key=NoteSorter.sorting_definitions[method]) == subdeck.notes)
