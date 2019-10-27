from dataclasses import field, dataclass
from pathlib import Path
from typing import Any

from .anki_deck_archiver import AnkiDeckArchiver
from .archiver import AllDeckArchiver
from .dulwich_repo import DulwichAnkiRepo
from ..anki.adapters.deck_manager import AnkiStaticDeckManager, DeckManager
from ..anki.ui.utils import progress_indicator
from ..export.anki_exporter import AnkiJsonExporter
from ..utils.notifier import Notifier, AnkiUiNotifier
from ..config.config_settings import ConfigSettings


@dataclass
class ArchiverVendor:
    window: Any
    config: ConfigSettings
    notifier: Notifier = field(default_factory=AnkiUiNotifier)

    @property
    def deck_manager(self) -> DeckManager:
        return AnkiStaticDeckManager(self.window.col.decks)

    def all_deck_archiver(self):
        return AllDeckArchiver(
            self.deck_manager,
            lambda deck: AnkiDeckArchiver(deck,
                                          self.snapshot_path().joinpath(self.window.pm.name),
                                          AnkiJsonExporter(self.window.col, self.config),
                                          DulwichAnkiRepo))

    def snapshot_path(self):
        return Path(self.config.snapshot_path)

    def do_manual_snapshot(self):
        self.do_snapshot('CrowdAnki: Manual snapshot')

    def snapshot_on_sync(self):
        self.do_snapshot('CrowdAnki: Snapshot on sync')

    def do_snapshot(self, reason):
        with progress_indicator(self.window, 'Taking CrowdAnki snapshot of all decks'):
            self.all_deck_archiver().archive(overrides=self.overrides(),
                                             reason=reason)
            self.notifier.info("Snapshot successful",
                               f"The CrowdAnki snapshot to {self.snapshot_path().resolve()} successfully completed")

    def overrides(self):
        return self.deck_manager.for_names(self.config.snapshot_root_decks)
