from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Callable

from .anki_repo import AnkiRepo
from .archiver import Archiver
from ..anki.adapters.anki_deck import AnkiDeck
from ..export.deck_exporter import DeckExporter


@dataclass
class AnkiDeckArchiver(Archiver):
    deck: AnkiDeck
    output_directory: Path
    deck_exporter: DeckExporter
    repo_provider: Callable[[Path], AnkiRepo]

    def archive(self, _: Iterable = tuple(), reason=None):
        deck_path = self.deck_exporter.export_to_directory(self.deck, self.output_directory)

        repo = self.repo_provider(deck_path)
        repo.stage_all()
        repo.commit(reason)
        repo.close()
