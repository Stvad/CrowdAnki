from functional import seq

from .deck import Deck
from .note import Note
from ..anki.adapters.anki_deck import AnkiDeck
from ..anki.adapters.note_model_file_provider import NoteModelFileProvider


def from_collection(collection, name, deck_metadata=None, is_child=False) -> Deck:
    decks = collection.decks
    # TODO Remove compatibility shims for Anki 2.1.46 and lower.
    by_name = decks.by_name if hasattr(decks, 'by_name') else decks.byName
    anki_dict = by_name(name)

    if AnkiDeck(anki_dict).is_dynamic:
        return None

    deck = Deck(NoteModelFileProvider, anki_dict, is_child)
    deck.collection = collection
    deck._update_fields()
    deck.metadata = deck_metadata
    deck._load_metadata()

    deck.notes = Note.get_notes_from_collection(collection, deck.anki_dict["id"], deck.metadata.models)

    direct_children = [child_name for child_name, _ in decks.children(deck.anki_dict["id"])
                       if Deck.DECK_NAME_DELIMITER
                       not in child_name[len(name) + len(Deck.DECK_NAME_DELIMITER):]]

    deck.children = seq(direct_children) \
        .map(lambda child_name: from_collection(collection, child_name, deck.metadata, True)) \
        .filter(lambda it: it is not None).order_by(lambda x: x.anki_dict["name"]).to_list()

    return deck


def from_json(json_dict, deck_metadata=None) -> Deck:
    """load metadata, load notes, load children"""
    deck = Deck(NoteModelFileProvider, json_dict)
    deck._update_fields()
    deck.metadata = deck_metadata

    if not deck.metadata:  # Todo mental check. The idea is that children don't have metadata
        deck._load_metadata_from_json(json_dict)

    deck.deck_config_uuid = json_dict["deck_config_uuid"]
    deck.notes = [Note.from_json(json_note) for json_note in json_dict["notes"]]
    deck.children = [from_json(child, deck_metadata=deck.metadata) for child in json_dict["children"]]

    deck.post_import_filter()

    return deck
