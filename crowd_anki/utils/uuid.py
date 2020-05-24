from dataclasses import dataclass

from functional import seq
from typing import List

from anki import Collection
from anki.notes import Note as AnkiNote
from ..utils.constants import UUID_FIELD_NAME


@dataclass
class UuidFetcher:
    collection: Collection

    def get_deck_config(self, uuid: str):
        return get_value_by_uuid(self.collection.decks.all_config(), uuid)

    def get_deck(self, uuid: str):
        return get_value_by_uuid(self.collection.decks.all(), uuid)

    def get_model(self, uuid: str):
        return get_value_by_uuid(self.collection.models.all(), uuid)

    def get_note(self, uuid: str):
        query = "select id from notes where guid=?"
        note_id = self.collection.db.scalar(query, uuid)
        if not note_id:
            return None

        return AnkiNote(self.collection, id=note_id)


def get_value_by_uuid(values: List, uuid: str):
    return seq(values).find(lambda it: it.get(UUID_FIELD_NAME) == uuid)
