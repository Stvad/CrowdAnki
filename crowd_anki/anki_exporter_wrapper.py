from pathlib import Path

import anki.hooks
import anki.exporting
import aqt.utils

from crowd_anki.anki_exporter import AnkiJsonExporter


class AnkiJsonExporterWrapper:
    """
    Wrapper designed to work with standard export dialog in anki.
    """

    key = "CrowdAnki Json representation"
    ext = ""
    hideTags = True
    directory_export = True

    def __init__(self, collection):
        self.includeMedia = True
        self.did = None
        self.count = 0 # Todo?
        self.collection = collection
        self.anki_json_exporter = AnkiJsonExporter(collection)

    def exportInto(self, directory_path):
        if self.did is None:
            aqt.utils.showWarning("CrowdAnki works only with specific decks.", title="Export failed")
            return 

        deck_name = self.collection.decks.get(self.did, default=False)["name"]
        self.anki_json_exporter.export_deck_to_directory(deck_name, Path(directory_path), self.includeMedia)


anki.hooks.addHook("exportersList",
                   lambda exporters_list: exporters_list.append(
                       anki.exporting.get_exporter_id(AnkiJsonExporterWrapper)))
