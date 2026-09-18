import os

from dataclasses import dataclass, field
from functional import seq
from typing import Any, Iterable, Set

from .file_provider import FileProvider


@dataclass
class NoteModelFileProvider(FileProvider):
    anki_collection: Any
    model_ids: Iterable[int]
    models: Iterable = field(init=False)

    def __post_init__(self):
        self.models = seq(self.model_ids) \
            .map(self.anki_collection.models.get) \
            .filter(lambda m: m is not None).to_list()

    def get_files(self) -> Set[str]:
        # TODO maybe switch to using
        # self.anki_collection.media.extract_static_media_files.  We
        # won't need belongs_to_any_model or _model_has_media, then.
        return seq(os.listdir(self.anki_collection.media.dir())) \
            .filter(lambda fn: fn.startswith("_")) \
            .filter(self.belongs_to_any_model) \
            .to_set()

    def belongs_to_any_model(self, file_name: str) -> bool:
        return seq(self.models) \
            .map(lambda model: _model_has_media(model, file_name)) \
            .any()

# Anki has removed pylib/anki/exporting.py. We are stealing this from
# there, from AnkiExporter._modelHasMedia (from the last existing
# version: de738fa15f73).
def _model_has_media(model, fname) -> bool:
    # First check the styling
    if fname in model["css"]:
        return True
    # If no reference to fname then check the templates as well
    for t in model["tmpls"]:
        if fname in t["qfmt"] or fname in t["afmt"]:
            return True
    return False
