from dataclasses import field
from pathlib import Path
from typing import Any

from .anki_deck_archiver import AnkiDeckArchiver
from .archiver import AllDeckArchiver
from .dulwich_repo import DulwichAnkiRepo
from ..anki.adapters.deck_manager import AnkiStaticDeckManager
from ..anki.ui.utils import progress_indicator
from ..dist.dataclasses import dataclass
from ..export.anki_exporter import AnkiJsonExporter
from ..utils.constants import USER_FILES_PATH


@dataclass
class ArchiverVendor:
    window: Any
    config: dict = field(init=False)

    def __post_init__(self):
        self.config = self.window.addonManager.getConfig(__name__)

    def all_deck_archiver(self):
        return AllDeckArchiver(AnkiStaticDeckManager(self.window.col.decks),
                               lambda deck: AnkiDeckArchiver(deck,
                                                             self.snapshot_path().joinpath(self.window.pm.name),
                                                             AnkiJsonExporter(self.window.col),
                                                             DulwichAnkiRepo))

    def snapshot_path(self):
        return Path(self.config.get('snapshot_path', str(USER_FILES_PATH.resolve())))

    def do_manual_snapshot(self):
        self.do_snapshot('Manual snapshot')

    def snapshot_on_sync(self):
        self.do_snapshot('Snapshot on sync')

    def do_snapshot(self, reason):
        with progress_indicator(self.window, 'Taking CrowdAnki snapshot of all decks'):
            self.all_deck_archiver().archive(reason=reason)
