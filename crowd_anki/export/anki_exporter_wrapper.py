from pathlib import Path

import aqt.utils
from .anki_exporter import AnkiJsonExporter
from ..anki.adapters.anki_deck import AnkiDeck
from ..utils import constants


class AnkiJsonExporterWrapper:
    """
    Wrapper designed to work with standard export dialog in anki.
    """

    key = "CrowdAnki Json representation"
    ext = constants.ANKI_EXPORT_EXTENSION
    hideTags = True
    includeTags = True
    directory_export = True

    def __init__(self, collection):
        self.includeMedia = True
        self.did = None
        self.count = 0  # Todo?
        self.collection = collection
        self.anki_json_exporter = AnkiJsonExporter(collection)

    # required by anki exporting interface with it's non PEP-8 names
    # noinspection PyPep8Naming
    def exportInto(self, directory_path):
        if self.did is None:
            aqt.utils.showWarning("CrowdAnki works only with specific decks.", title="Export failed")
            return

        deck = AnkiDeck(self.collection.decks.get(self.did, default=False))
        self.anki_json_exporter.export_to_directory(deck, Path(directory_path).parent, self.includeMedia)
        # .parent because we receive name with random numbers at the end (hacking around internals of Anki) :(

        self.count = self.anki_json_exporter.last_exported_count


def get_exporter_id(exporter):
    return f"{exporter.key} (*{exporter.ext})", exporter


def exporters_hook(exporters_list):
    exporter_id = get_exporter_id(AnkiJsonExporterWrapper)
    if exporter_id not in exporters_list:
        exporters_list.append(exporter_id)
