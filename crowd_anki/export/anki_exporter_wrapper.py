from pathlib import Path

from .anki_exporter import AnkiJsonExporter
from ..anki.adapters.anki_deck import AnkiDeck
from ..utils import constants
from ..utils.notifier import AnkiUiNotifier, Notifier

EXPORT_FAILED_TITLE = "Export failed"


class AnkiJsonExporterWrapper:
    """
    Wrapper designed to work with standard export dialog in anki.
    """

    key = "CrowdAnki JSON representation"
    ext = constants.ANKI_EXPORT_EXTENSION
    hideTags = True
    includeTags = True
    directory_export = True

    def __init__(self, collection,
                 deck_id: int = None,
                 json_exporter: AnkiJsonExporter = None,
                 notifier: Notifier = None):
        self.includeMedia = True
        self.did = deck_id
        self.count = 0  # Todo?
        self.collection = collection
        self.anki_json_exporter = json_exporter or AnkiJsonExporter(collection)
        self.notifier = notifier or AnkiUiNotifier()

    # required by anki exporting interface with it's non PEP-8 names
    # noinspection PyPep8Naming
    def exportInto(self, directory_path):
        if self.did is None:
            self.notifier.warning(EXPORT_FAILED_TITLE, "CrowdAnki export works only for specific decks. "
                                                       "Please use CrowdAnki snapshot if you want to export "
                                                       "the whole collection.")
            return

        deck = AnkiDeck(self.collection.decks.get(self.did, default=False))
        if deck.is_dynamic:
            self.notifier.warning(EXPORT_FAILED_TITLE, "CrowdAnki does not support export for dynamic decks.")
            return

        # .parent because we receive name with random numbers at the end (hacking around internals of Anki) :(
        export_path = Path(directory_path).parent
        self.anki_json_exporter.export_to_directory(deck, export_path, self.includeMedia)

        self.count = self.anki_json_exporter.last_exported_count


def get_exporter_id(exporter):
    return f"{exporter.key} (*{exporter.ext})", exporter


def exporters_hook(exporters_list):
    exporter_id = get_exporter_id(AnkiJsonExporterWrapper)
    if exporter_id not in exporters_list:
        exporters_list.append(exporter_id)
