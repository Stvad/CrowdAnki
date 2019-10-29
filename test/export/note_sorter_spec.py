from mamba import describe, it, context, before
from unittest.mock import MagicMock
from random import shuffle

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.export.note_sorter import NoteSorter
from crowd_anki.config.config_settings import ConfigSettings


test_guids = ["abc", "bcd", "cde", "def", "efg", "fgh"]
test_flags = [0, 1, 2, 3, 4, 5]
test_tags = ["adjectives", "directions", "interesting", "nouns", "verbs", "zzzzFinal"]
test_notemodels = ["Default", "LL Noun", "LL Sentence", "LL Verb", "LL Word", "Zulu"]
test_notemodelids = test_guids
test_fields = test_tags


class NoteSorterTester():
    def __init__(self):
        self.notes = self.setup_notes()

        self.config = ConfigSettings(False)
        self.config.export_deck_sort_reversed = False

    def get_single_note_mock(self, i):
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

        return notes_list
    
    def set_sort_method(self, set_to):
        self.config.export_deck_sort_methods = set_to
    
    def setup(self):
        self.notesorter = NoteSorter(self.config)
        self.sorted_notes = self.notesorter.sort_notes(self.notes)
    
with describe(NoteSorterTester) as self:
    with before.each:
        self.tester = NoteSorterTester()

 
    with context("user sorts by each sort option"):
        with it("do not sort / sort by none"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.NO_SORTING.value])

            self.tester.setup()

            assert(self.tester.sorted_notes == self.tester.notes)

        with it("sort by guid"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.GUID.value])
            
            self.tester.setup()

            assert([note.anki_object.guid for note in self.tester.sorted_notes] == test_guids)

        with it("sort by flag"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.FLAG.value])

            self.tester.setup()

            assert([note.anki_object.flags for note in self.tester.sorted_notes] == test_flags)

        with it("sort by tag"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.TAG.value])

            self.tester.setup()

            assert([note.anki_object.tags for note in self.tester.sorted_notes] == test_tags)

        with it("sort by notemodel"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.NOTE_MODEL.value])

            self.tester.setup()

            assert([note.anki_object._model["name"] for note in self.tester.sorted_notes] == test_notemodels)

        with it("sort by notemodelid"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.NOTE_MODEL_ID.value])

            self.tester.setup()

            assert([note.anki_object._model["crowdanki_uuid"] for note in self.tester.sorted_notes] == test_notemodelids)

        with it("sort by field1"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.FIELD1.value])

            self.tester.setup()

            assert([note.anki_object.fields[0] for note in self.tester.sorted_notes] == test_fields)

        with it("sort by field2"):
            self.tester.set_sort_method([ConfigSettings.DeckExportSortMethods.FIELD2.value])

            self.tester.setup()

            assert([note.anki_object.fields[1] for note in self.tester.sorted_notes] == test_fields)

