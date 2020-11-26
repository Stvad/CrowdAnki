import logging
from random import shuffle
from unittest.mock import MagicMock

from aqt import mw
from mamba import describe, it, context

from crowd_anki.config.config_settings import ConfigSettings, NoteSortingMethods
from crowd_anki.export.note_sorter import NoteSorter

test_guids = ["abc", "bcd", "cde", "def", "efg", "fgh"]
test_flags = [0, 1, 2, 3, 4, 5]
test_tags = ["adjectives", "directions10", "directions2", "nouns", "verbs", "zzzzFinal"]
test_tags_numeric = [["adjectives"], ["directions", 2], ["directions", 10], ["nouns"],
                     ["verbs"], ["zzzzFinal"]]
test_note_ids = test_flags
test_notemodels = ["Default", "LL Noun", "LL Sentence", "LL Verb", "LL Word", "Zulu"]
test_notemodelids = test_guids
test_fields = test_tags
test_fields_numeric = test_tags_numeric
test_sortf = [0] * 6

note_sorting_single_result_pairs = [
    (NoteSortingMethods.GUID, test_guids),
    (NoteSortingMethods.FLAG, test_flags),
    (NoteSortingMethods.TAG, test_tags),
    (NoteSortingMethods.TAG_N, test_tags_numeric),
    (NoteSortingMethods.NOTE_ID, test_note_ids),
    (NoteSortingMethods.NOTE_MODEL_NAME, test_notemodels),
    (NoteSortingMethods.NOTE_MODEL_ID, test_notemodelids),
    (NoteSortingMethods.FIELD1, test_fields),
    (NoteSortingMethods.FIELD1_N, test_fields_numeric),
    (NoteSortingMethods.FIELD2, test_fields),
    (NoteSortingMethods.FIELD_LAST, test_fields),
    (NoteSortingMethods.BROWSER_SORT_FIELD, test_fields)
]

test_multikey_notemodel_guid = [(notemodel, guid) for notemodel in test_notemodels for guid in test_guids]


class NoteSorterTester:
    def __init__(self):
        self.note_sorter = None
        self.notes = []
        self.sorted_notes = []

        self.config = ConfigSettings(mw.addonManager)

    @staticmethod
    def get_single_note_mock(i):
        note = MagicMock()

        note.anki_object.guid = test_guids[i]
        note.anki_object.flags = test_flags[i]
        note.anki_object.tags = test_tags[i]
        note.anki_object.id = test_note_ids[i]

        note.anki_object._model = {
            "name": test_notemodels[i],
            "crowdanki_uuid": test_notemodelids[i],
            "sortf": test_sortf[i]
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

    def setup_notes(self, is_multi_key: bool):
        random_range = list(range(0, len(test_multikey_notemodel_guid if is_multi_key else test_guids)))
        shuffle(random_range)

        if is_multi_key:
            notes_list = [self.get_multikey_note_mock(i) for i in random_range]
        else:
            notes_list = [self.get_single_note_mock(i) for i in random_range]

        logging.info("Shuffled list: ", notes_list)

        self.notes = notes_list

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
