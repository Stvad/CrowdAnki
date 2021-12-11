from dataclasses import field, dataclass
from pathlib import Path
from typing import Any

from .anki_deck_archiver import AnkiDeckArchiver
from .archiver import AllDeckArchiver
from .dulwich_repo import DulwichAnkiRepo
from ..anki.adapters.deck_manager import AnkiStaticDeckManager, DeckManager
from ..anki.ui.utils import progress_indicator
from ..config.config_settings import ConfigSettings
from ..export.anki_exporter import AnkiJsonExporter
from ..utils.notifier import Notifier, AnkiTooltipNotifier
from ..utils.disambiguate_uuids import disambiguate_note_model_uuids


@dataclass
class ArchiverVendor:
    window: Any
    config: ConfigSettings
    notifier: Notifier = field(default_factory=AnkiTooltipNotifier)

    @property
    def deck_manager(self) -> DeckManager:
        return AnkiStaticDeckManager(self.window.col.decks)

    def all_deck_archiver(self):
        return AllDeckArchiver(
            self.deck_manager,
            lambda deck: AnkiDeckArchiver(deck,
                                          self.config.full_snapshot_path,
                                          AnkiJsonExporter(self.window.col, self.config),
                                          DulwichAnkiRepo))

    def snapshot_path(self):
        return Path(self.config.snapshot_path)

    def do_manual_snapshot(self):
        self.do_snapshot('CrowdAnki: Manual snapshot')

    def snapshot_on_sync(self):
        if self.config.automated_snapshot:
            self.do_snapshot('CrowdAnki: Snapshot on sync')

    def do_snapshot(self, reason):
        # Clean up duplicate note models. See
        # https://github.com/Stvad/CrowdAnki/wiki/Workarounds-%E2%80%94-Duplicate-note-model-uuids.
        disambiguate_note_model_uuids(self.window.col)

        with progress_indicator(self.window, 'Taking CrowdAnki snapshot of all decks'):
            self.all_deck_archiver().archive(overrides=self.overrides(),
                                             reason=reason)
            self.notifier.info("Snapshot successful",
                               f"The CrowdAnki snapshot to {str(self.config.full_snapshot_path)} successfully completed")

    def overrides(self):
        return self.deck_manager.for_names(self.config.snapshot_root_decks)
