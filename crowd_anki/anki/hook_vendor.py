from dataclasses import dataclass, field
from typing import Any

from ..anki.adapters.hook_manager import AnkiHookManager
from ..export.anki_exporter_wrapper import exporters_hook
from ..history.archiver_vendor import ArchiverVendor
from ..utils.config import AUTOMATED_SNAPSHOT


@dataclass
class HookVendor:
    window: Any
    hook_manager: AnkiHookManager = AnkiHookManager()
    config: dict = field(init=False)

    def __post_init__(self):
        self.config = self.window.addonManager.getConfig(__name__)

    def setup_hooks(self):
        self.setup_exporter_hook()
        self.setup_snapshot_hooks()

    def setup_exporter_hook(self):
        self.hook_manager.hook("exportersList", exporters_hook)

    def setup_snapshot_hooks(self):
        if not self.config.get(AUTOMATED_SNAPSHOT, False):
            return

        snapshot_handler = ArchiverVendor(self.window).snapshot_on_sync
        self.hook_manager.hook('profileLoaded', snapshot_handler)
        self.hook_manager.hook('unloadProfile', snapshot_handler)
