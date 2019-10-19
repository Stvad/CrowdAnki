from mamba import describe, it, context
from unittest.mock import MagicMock

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.export.note_sorter import sort_notes

DUMMY_EXPORT_DIRECTORY = "/tmp"

TEST_DECK_ID = 1

CONFIG_NO_SORTING = {
    "config": {
        "export_deck_sort": {
            "method": ["none"],
            "reversed": False
        }
    }
}

CONFIG_SORT_BY_THREE = {
    "config": {
        "export_deck_sort": {
            "method": ["notemodels", "firstfield", "guid"],
            "reversed": False
        }
    }
}

def get_single_note_mock():
    note = MagicMock()

    note.export_filter_set.get.return_value = {}

    # anki_object.guid
    # anki_object.flags
    # anki_object.tags
    # anki_object._model["name"]
    # anki_object._model["crowdanki_uuid"]
    # anki_object.fields[0]

    return note

def setup_notes():
    notes_list = get_single_note_mock()



    return notes_list

with describe(AnkiJsonExporter) as self:
    with context("user selects no filtering options"):
        with it("does not filter the notes, returning the same value as passed in"):
            collection_mock = MagicMock()

            notes = setup_notes()

            config_mock = MagicMock()
            config_mock.return_value = CONFIG_NO_SORTING

            subject = AnkiJsonExporter(collection_mock, config_mock)
            sorted_notes = subject.sort_notes(notes)

            assert(sorted_notes == notes)


