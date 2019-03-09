from dataclasses import field, dataclass
from pathlib import Path
from typing import Any

from .anki_deck_archiver import AnkiDeckArchiver
from .archiver import AllDeckArchiver
from .dulwich_repo import DulwichAnkiRepo
from ..anki.adapters.deck_manager import AnkiStaticDeckManager, DeckManager
from ..anki.ui.utils import progress_indicator
from ..export.anki_exporter import AnkiJsonExporter
from ..utils.config import SNAPSHOT_ROOT_DECKS
from ..utils.constants import USER_FILES_PATH


@dataclass
class ArchiverVendor:
    window: Any
    config: dict = field(init=False)

    def __post_init__(self):
        self.config = self.window.addonManager.getConfig(__name__)

    @property
    def deck_manager(self) -> DeckManager:
        return AnkiStaticDeckManager(self.window.col.decks)

    def all_deck_archiver(self):
        return AllDeckArchiver(
            self.deck_manager,
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
            self.all_deck_archiver().archive(overrides=self.overrides(),
                                             reason=reason)

    def overrides(self):
        return self.deck_manager.for_names(self.config.get(SNAPSHOT_ROOT_DECKS))
