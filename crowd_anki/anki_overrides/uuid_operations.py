from anki.notes import Note as AnkiNote
from anki.decks import DeckManager
from anki.models import ModelManager
from ..utils.constants import UUID_FIELD_NAME


# AnkiNote
def get_note_bu_uuid(cls, collection, uuid):
    query = "select id from notes where guid=?"
    note_id = collection.db.scalar(query, uuid)
    if not note_id:
        return None

    return cls(collection, id=note_id)


# Todo: consider introducing cache for the functions below
# It was not introduced initially because there is no convenient way to update it right now
# and number of considered objects are unlikely to be big.


def get_from_dict_by_uuid(base_object, dict_name, uuid):
    for value in (getattr(base_object, dict_name)).values():
        if value.get(UUID_FIELD_NAME) == uuid:
            return value

    return None


# Deck
def get_deck_by_uuid(self, uuid):
    return get_from_dict_by_uuid(self, "decks", uuid)


# Deck configuration
def get_deck_configuration_by_uuid(self, uuid):
    return get_from_dict_by_uuid(self, "dconf", uuid)


# Note model
def get_note_model_by_uuid(self, uuid):
    return get_from_dict_by_uuid(self, "models", uuid)


# Insertion
AnkiNote.get_by_uuid = classmethod(get_note_bu_uuid)

DeckManager.get_deck_by_uuid = get_deck_by_uuid
DeckManager.get_deck_config_by_uuid = get_deck_configuration_by_uuid

ModelManager.get_by_uuid = get_note_model_by_uuid
