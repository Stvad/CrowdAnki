from abc import abstractmethod, ABC

from pathlib import Path

from ..anki.adapters.anki_deck import AnkiDeck


class DeckExporter(ABC):
    @abstractmethod
    def export_to_directory(self, deck: AnkiDeck, output_dir: Path, copy_media=True) -> Path:
        pass
