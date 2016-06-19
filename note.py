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
        self.anki_object = None

    @staticmethod
    # Todo:
    # Bad, need to switch to API usage if ever available. As an option - implement them myself.
    def get_cards_from_db(db, deck_id):
        return db.list(
            "SELECT id FROM cards WHERE did=? OR odid=?", deck_id, deck_id)

    @staticmethod
    def get_notes_from_collection(collection, deck_id):
        card_ids_str = anki.utils.ids2str(Note.get_cards_from_db(collection.db, deck_id))
        note_id_set = set(collection.db.list("SELECT nid FROM cards WHERE id IN " + card_ids_str))
        return [Note.from_collection(collection, note_id) for note_id in note_id_set]

    @classmethod
    def from_collection(cls, collection, note_id):
        note = Note()
        note.anki_object = AnkiNote(collection, id=note_id)
        return note
