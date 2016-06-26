from uuid import uuid1

import anki
from anki.notes import Note as AnkiNote

from CrowdAnki import utils
from CrowdAnki.json_serializable import JsonSerializableAnkiObject
from CrowdAnki.common_constants import UUID_FIELD_NAME


class Note(JsonSerializableAnkiObject):
    filter_set = JsonSerializableAnkiObject.filter_set | \
                 {"col",  # Don't need collection
                  "_fmap",  # Generated data
                  "_model"  # Card model. Would be handled by deck. uuid?
                  }

    def __init__(self, anki_note=None):
        super(Note, self).__init__(anki_note)

    @staticmethod
    # Todo:
    # Bad, need to switch to API usage if ever available. As an option - implement them myself.
    def get_cards_from_db(db, deck_id):
        return db.list(
            "SELECT id FROM cards WHERE did=? OR odid=?", deck_id, deck_id)

    @staticmethod
    def get_notes_from_collection(collection, deck_id):
        card_ids_str = anki.utils.ids2str(Note.get_cards_from_db(collection.db, deck_id))
        note_ids = collection.db.list("SELECT DISTINCT nid FROM cards WHERE id IN " + card_ids_str)
        return [Note.from_collection(collection, note_id) for note_id in note_ids]

    @classmethod
    def from_collection(cls, collection, note_id):
        anki_note = AnkiNote(collection, id=note_id)
        note = Note(anki_note)
        return note
