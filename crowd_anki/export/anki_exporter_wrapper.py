from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing import TYPE_CHECKING

from aqt.import_export.exporting import Exporter, ExportOptions

from aqt.utils import tr, tooltip

if TYPE_CHECKING:
    import aqt.main
    from anki.collection import Collection
    from anki.decks import DeckId

from .anki_exporter import AnkiJsonExporter
from ..anki.adapters.anki_deck import AnkiDeck
from ..config.config_settings import ConfigSettings
from ..utils import constants
from ..utils.notifier import AnkiModalNotifier, Notifier
from ..utils.disambiguate_uuids import disambiguate_note_model_uuids
from ..errors import UnexportableDeckException

EXPORT_FAILED_TITLE = "Export failed"
EXPORT_KEY = "CrowdAnki JSON representation" # TODO make this localisable, like in Anki (tr.(...))


class AnkiJsonExporterWrapper(Exporter):
    """Wrapper to work with standard export dialog in anki 2.1.55+."""
    extension = constants.ANKI_EXPORT_EXTENSION
    show_deck_list = True
    show_include_media = True

    @staticmethod
    def name() -> str:
        return EXPORT_KEY

    def export(self, mw: aqt.main.AnkiQt,
               options: ExportOptions,
               anki_json_exporter: AnkiJsonExporter = None,
               notifier: Notifier = None) -> None:

        def on_success(count: int) -> None:
            """Display a tooltip with the number of exported notes.

            Copied from aqt/import_export/exporting.py.

            """
            # # TODO decide if we want other add-ons to be called on CrowdAnki export
            # gui_hooks.exporter_did_export(options, self)
            tooltip(tr.exporting_card_exported(count=count), parent=mw)

        if options.limit is None:
            deck_id = None
        else:
            deck_id = options.limit.deck_id

        if anki_json_exporter is None:
            anki_json_exporter = AnkiJsonExporter(mw.col, ConfigSettings.get_instance())
        if notifier is None:
            notifier = AnkiModalNotifier()

        try:
            deck = AnkiJsonExporterWrapper.return_deck_or_reject(mw.col, deck_id, notifier)
        except UnexportableDeckException:
            return

        count = AnkiJsonExporterWrapper.clean_up_and_export(
            options.out_path, mw.col, deck, options.include_media, anki_json_exporter,
        )

        on_success(count)

    @staticmethod
    def return_deck_or_reject(collection: Collection,
                              deck_id: Optional[DeckId],
                              notifier: Notifier) -> AnkiDeck:

        """Return deck from deck_id.  Reject "all" and filtered decks."""
        if deck_id is None:
            notifier.warning(EXPORT_FAILED_TITLE, "CrowdAnki export works only for specific decks. "
                             "Please use CrowdAnki snapshot if you want to export "
                             "the whole collection.")
            raise UnexportableDeckException

        deck = AnkiDeck(collection.decks.get(deck_id, default=False))
        if deck.is_dynamic:
            notifier.warning(EXPORT_FAILED_TITLE, "CrowdAnki does not support export for dynamic decks.")
            raise UnexportableDeckException

        return deck

    @staticmethod
    def clean_up_and_export(directory_path: str,
                            collection: Collection,
                            deck: AnkiDeck,
                            include_media: bool,
                            anki_json_exporter: AnkiJsonExporter) -> int:
        """Clean up and do the actual export.

        Also, return the exported note count, for instance, for
        displaying in a tooltip.

        """
        # Clean up duplicate note models. See
        # https://github.com/Stvad/CrowdAnki/wiki/Workarounds-%E2%80%94-Duplicate-note-model-uuids.
        disambiguate_note_model_uuids(collection)

        # .parent because we receive name with random numbers at the end (hacking around internals of Anki) :(
        export_path = Path(directory_path).parent
        anki_json_exporter.export_to_directory(
            deck, export_path, include_media,
            create_deck_subdirectory=ConfigSettings.get_instance().export_create_deck_subdirectory
        )

        return anki_json_exporter.last_exported_count

def exporters_hook(exporters_list):
    """Exporter hook for exporters_list_did_initialize."""
    if not AnkiJsonExporterWrapper in exporters_list:
        exporters_list.append(AnkiJsonExporterWrapper)
