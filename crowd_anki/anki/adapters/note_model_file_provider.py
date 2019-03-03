import os

from dataclasses import dataclass, field
from functional import seq
from typing import Any, Iterable, Set

from anki.exporting import AnkiExporter
from .file_provider import FileProvider


@dataclass
class NoteModelFileProvider(FileProvider):
    anki_collection: Any
    model_ids: Iterable[int]
    models: Iterable = field(init=False)
    anki_exporter: AnkiExporter = field(init=False)

    def __post_init__(self):
        self.anki_exporter = AnkiExporter(self.anki_collection)
        self.models = seq(self.model_ids) \
            .map(self.anki_collection.models.get) \
            .filter(lambda m: m is not None).to_list()

    def get_files(self) -> Set[str]:
        return seq(os.listdir(self.anki_collection.media.dir())) \
            .filter(lambda fn: fn.startswith("_")) \
            .filter(self.belongs_to_any_model) \
            .to_set()

    def belongs_to_any_model(self, file_name: str) -> bool:
        return seq(self.models) \
            .map(lambda model: self.anki_exporter._modelHasMedia(model, file_name)) \
            .any()
