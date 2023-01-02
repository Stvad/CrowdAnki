"""Compat for Anki 2.1.54-

This is copied verbatim from `qt/aqt/import_export/exporting.py` (in
Anki 2.1.55).  We need it for our tests, which still assume that we
have Anki 2.1.26 and where the above module is missing.  We can't
upgrade our dependency to Anki 2.1.55 which has the module, because
we're still using Python 3.7 with which latest Anki is incompatible.

We could instead mock the imports from aqt.import_export.exporting
(Exporter), but given that AnkiJsonExporterWrapperNew inherits from
Exporter, this feels a bit too magical.  Also, using the way in this
file, we keep compatibility for Anki 2.1.50+ (the oldest we support
atm), for a while longer.

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import Any

import aqt.main

ExportLimit = Any

@dataclass
class ExportOptions:
    out_path: str
    include_scheduling: bool
    include_media: bool
    include_tags: bool
    include_html: bool
    include_deck: bool
    include_notetype: bool
    include_guid: bool
    legacy_support: bool
    limit: ExportLimit

class Exporter(ABC):
    extension: str
    show_deck_list = False
    show_include_scheduling = False
    show_include_media = False
    show_include_tags = False
    show_include_html = False
    show_legacy_support = False
    show_include_deck = False
    show_include_notetype = False
    show_include_guid = False

    @abstractmethod
    def export(self, mw: aqt.main.AnkiQt, options: ExportOptions) -> None:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass
