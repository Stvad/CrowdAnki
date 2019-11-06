import logging

from mamba import describe, it, context
from unittest.mock import MagicMock
from random import shuffle

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.config.config_settings import ConfigSettings, NoteSortingMethods


with describe(ConfigSettings) as self:
    with context("someone interacts with any config setting"):
        with it("do not sort / sort by none"):
            config = ConfigSettings({
                "automated_snapshot": True
            })

            assert config.automated_snapshot

        with it("tries to find the invalid config entries"):
            config = ConfigSettings()

            valid_sorting_methods = list(NoteSortingMethods.values())
            assert len(valid_sorting_methods) > 0

            invalid_examples = ["testing", "giud", "dan", "flags", "notemodels", "feild", "card", "note"]

            config.export_note_sort_methods = invalid_examples + valid_sorting_methods
            assert (len(valid_sorting_methods) + len(invalid_examples)) == len(config.export_note_sort_methods)

            results = config.find_invalid_config_values()

            assert results == invalid_examples

        with it("should set the empty textboxes to their default values"):
            config = ConfigSettings({
                "export_note_sort_methods": [""],
                "snapshot_path": ""
            })

            config.handle_empty_textboxes()

            assert config.export_note_sort_methods == config.Properties.EXPORT_NOTE_SORT_METHODS.value.default_value
            assert config.snapshot_path == config.Properties.SNAPSHOT_PATH.value.default_value

        with it("tries to save"):
            config = ConfigSettings({
                "snapshot_path": "testing",
                "automated_snapshot": True,
                "snapshot_root_decks": ["TestDeck1", "Other"],
                "export_notes_reverse_order": True,
                "export_note_sort_methods": ["notemodel", "guid"]
            })

            config.save()

            print(config._config["snapshot_path"])

            assert config._config["snapshot_path"] == config.snapshot_path
            assert config._config["automated_snapshot"] == config.automated_snapshot
            assert config._config["snapshot_root_decks"] == config.snapshot_root_decks
            assert config._config["export_notes_reverse_order"] == config.export_notes_reverse_order
            assert config._config["export_note_sort_methods"] == config.export_note_sort_methods
