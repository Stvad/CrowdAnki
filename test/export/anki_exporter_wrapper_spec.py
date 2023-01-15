from unittest.mock import MagicMock

from mamba import describe, it, context

from test_utils.anki import MockAnkiModules

mock_anki_modules = MockAnkiModules(["win32file", "win32pipe", "pywintypes", "winerror"]) # Anki on Windows uses pywin32

from crowd_anki.export.anki_exporter_wrapper import AnkiJsonExporterWrapper, AnkiJsonExporterWrapperNew

DUMMY_EXPORT_DIRECTORY = "/tmp"

TEST_DECK_ID = 1

with describe(AnkiJsonExporterWrapper) as self:
    with context("user is trying to export dynamic deck"):
        with it("should warn and exit without initiating export"):
            exporter_mock = MagicMock()
            notifier_mock = MagicMock()

            collection_mock = MagicMock()
            collection_mock.decks.get.return_value = {'dyn': True}

            subject = AnkiJsonExporterWrapper(collection_mock, TEST_DECK_ID, exporter_mock, notifier_mock)

            subject.exportInto(DUMMY_EXPORT_DIRECTORY)

            notifier_mock.warning.assert_called_once()
            exporter_mock.export_to_directory.assert_not_called()

with describe(AnkiJsonExporterWrapperNew) as self:
    with context("user is trying to export dynamic deck"):
        with it("should warn and exit without initiating export"):
            mw_mock = MagicMock()
            mw_mock.col.decks.get.return_value = {'dyn': True}

            options_mock = MagicMock()
            exporter_mock = MagicMock()
            notifier_mock = MagicMock()

            subject = AnkiJsonExporterWrapperNew()
            subject.export(mw_mock, options_mock, exporter_mock, notifier_mock)

            notifier_mock.warning.assert_called_once()
            exporter_mock.export_to_directory.assert_not_called()

mock_anki_modules.unmock()
