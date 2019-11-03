import logging

from mamba import describe, it, context
from unittest.mock import MagicMock
from random import shuffle

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.export.note_sorter import NoteSorter
from crowd_anki.config.config_settings import ConfigSettings, NoteSortingMethods

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
    (NoteSortingMethods.NOTE_MODEL, test_notemodels),
    (NoteSortingMethods.NOTE_MODEL_ID, test_notemodelids),
    (NoteSortingMethods.FIELD1, test_fields),
    (NoteSortingMethods.FIELD2, test_fields)
]


class NoteSorterTester:
    def __init__(self):
        self.note_sorter = None
        self.notes = self.setup_notes()
        self.sorted_notes = []

        self.config = ConfigSettings()

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

    def setup_notes(self):
        random_range = list(range(0, len(test_guids)))
        shuffle(random_range)
        notes_list = [self.get_single_note_mock(i) for i in random_range]

        logging.info("Shuffled list: ", notes_list)

        return notes_list

    def sort_with(self, sort_methods, reverse_sort):
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

        with it("sorts by all sorting methods, reversed"):
            for method, result in note_sorting_single_result_pairs:
                self.tester = NoteSorterTester()

                self.tester.sort_with([method], True)

                assert ([NoteSorter.sorting_definitions[method](note) for note in self.tester.sorted_notes
                         ] == list(reversed(result)))
