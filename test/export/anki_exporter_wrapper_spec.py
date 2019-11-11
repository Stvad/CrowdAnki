from mamba import describe, it, context
from unittest.mock import MagicMock

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.export.anki_exporter_wrapper import AnkiJsonExporterWrapper

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
