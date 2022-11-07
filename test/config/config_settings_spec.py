from unittest.mock import MagicMock

from expects import expect, contain
from mamba import describe, it, context

from test_utils.anki import MockAnkiModules

mock_anki_modules = MockAnkiModules()

from aqt import mw

from crowd_anki.config.config_settings import ConfigSettings, NoteSortingMethods

with describe(ConfigSettings) as self:
    with context("someone interacts with any config setting"):
        with it("do not sort / sort by none"):
            config = ConfigSettings(mw.addonManager, {
                "automated_snapshot": True
            })

            assert config.automated_snapshot

        with it("get all the NoteSortingMethod values"):
            valid_sorting_methods = list(NoteSortingMethods.values())
            assert len(valid_sorting_methods) > 0
            assert isinstance(valid_sorting_methods, list)

        with it("tries to find the invalid config entries"):
            config = ConfigSettings(mw.addonManager)

            valid_sorting_methods = list(NoteSortingMethods.values())

            invalid_examples = ["testing", "giud", "dan", "flags", "notemodels", "feild", "card", "note"]

            config.export_note_sort_methods = invalid_examples + valid_sorting_methods

            results = config.find_invalid_config_values()

            assert results == invalid_examples

        with it("should set the empty properties to their default values"):
            config = ConfigSettings(init_values={
                "export_note_sort_methods": [""],
                "snapshot_path": ""
            })

            config.try_infer_values()

            assert config.export_note_sort_methods == config.Properties.EXPORT_NOTE_SORT_METHODS.value.default_value
            assert config.snapshot_path == config.Properties.SNAPSHOT_PATH.value.default_value

        with it("tries to load to initial values in the constructor"):
            settings = {
                "snapshot_path": "testing",
                "automated_snapshot": True,
                "snapshot_root_decks": ["TestDeck1", "Other"],
                "export_notes_reverse_order": True,
                "export_note_sort_methods": ["notemodel", "guid"]
            }

            config = ConfigSettings(init_values=settings)

            assert config._config == settings

            for key in settings:
                assert settings[key] == getattr(config, key)

        with it("tries to save new values to config dictionary"):
            addon_manager_mock = MagicMock()

            old_settings = {
                "snapshot_path": "",
                "automated_snapshot": False,
                "snapshot_root_decks": [],
                "export_notes_reverse_order": False,
                "export_note_sort_methods": [],
                "import_notes_ignore_deck_movement": False
            }

            new_settings = {
                "snapshot_path": "testing",
                "automated_snapshot": True,
                "snapshot_root_decks": ["TestDeck1", "Other"],
                "export_notes_reverse_order": True,
                "export_note_sort_methods": ["notemodel", "guid"],
                "import_notes_ignore_deck_movement": True
            }

            config = ConfigSettings(addon_manager_mock, old_settings, MagicMock())

            for key in new_settings:
                setattr(config, key, new_settings[key])

            config.save()

            expect(config._config.items()).to(contain(*list(new_settings.items())))
            addon_manager_mock.writeConfig.assert_called_once()

mock_anki_modules.unmock()
