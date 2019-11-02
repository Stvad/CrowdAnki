from dataclasses import dataclass
from typing import Any

from ..config.config_settings import ConfigSettings
from ..anki.adapters.hook_manager import AnkiHookManager
from ..export.anki_exporter_wrapper import exporters_hook
from ..history.archiver_vendor import ArchiverVendor


@dataclass
class HookVendor:
    window: Any
    config: ConfigSettings
    hook_manager: AnkiHookManager = AnkiHookManager()

    def setup_hooks(self):
        self.setup_exporter_hook()
        self.setup_snapshot_hooks()

    def setup_exporter_hook(self):
        self.hook_manager.hook("exportersList", exporters_hook)

    def setup_snapshot_hooks(self):
        if not self.config.automated_snapshot:
            return

        snapshot_handler = ArchiverVendor(self.window, self.config).snapshot_on_sync
        self.hook_manager.hook('profileLoaded', snapshot_handler)
        self.hook_manager.hook('unloadProfile', snapshot_handler)
