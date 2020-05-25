from dataclasses import dataclass, field
from typing import Callable, Any, Optional

from ...github.github_importer import GitImporter
from ...history.archiver_vendor import ArchiverVendor
from ...importer.anki_importer import AnkiJsonImporter
from ...config.config_settings import ConfigSettings


@dataclass
class ActionVendor:
    window: Any
    config: ConfigSettings
    action_supplier: Callable[[str, Any], Any]
    directory_vendor: Callable[[str], Optional[str]]
    archiver_vendor: ArchiverVendor = field(init=False)

    def __post_init__(self):
        self.archiver_vendor = ArchiverVendor(self.window, self.config)

    def action(self, name, handler):
        action = self.action_supplier(name, self.window)
        action.triggered.connect(handler)
        return action

    def actions(self):
        return [self.import_action(), self.github_import(), self.snapshot()]

    def import_action(self):
        return self.action('CrowdAnki: Import from disk',
                           lambda: AnkiJsonImporter.import_deck(self.window.col, self.directory_vendor))

    def github_import(self):
        return self.action("CrowdAnki: Import git repository",
                           lambda: GitImporter.on_git_import_action(self.window.col))

    def snapshot(self):
        return self.action('CrowdAnki: Snapshot', self.archiver_vendor.do_manual_snapshot)
