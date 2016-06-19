import json
from pprint import pprint
import os.path

import anki
from anki.notes import Note as AnkiNote
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import QAction, SIGNAL

from anki import Collection
from reportlab.lib.validators import isInstanceOf

import db_util
from utils import merge_dicts

COLLECTION_PATH = "../WCollection/collection.anki2"

UUID_FIELD_NAME = "crowdanki_uuid"


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)


# create a new menu item, "test"
# action = QAction("test", mw)
# set it to call testFunction when it's clicked
# mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
# mw.form.menuTools.addAction(action)


class JsonExporter(object):
    def __init__(self, collection):  # Todo default parameter current running collection
        self.collection = collection

        # for deck in self.collection.decks.all():
        #     pprint(deck)

        deck_name = "tdeckl1"

        # for note in self.collection.findNotes('"deck:Software::Bash::Shell navigation"'):
        #     pprint(note)

        pprint(self.get_note_ids(deck_name))
        pprint(self.get_note_ids_find(deck_name))

        pprint([note._model for note in self.get_notes(deck_name)][0])
        # pprint([note.data for note in self.get_notes("Rationality") if note.data])

        deck_id = self.collection.decks.byName(deck_name)["id"]
        # pprint(self.collection.decks.confForDid(deck_id))

    def export_deck(self, deck_id):
        """Returns json for given deck and list of dependencies"""
        working_deck = self.collection.decks.get(deck_id)

        for child in working_deck.children():
            pass

    def get_notes(self, deck_name):
        return [AnkiNote(self.collection, id=note_id) for note_id in self.get_note_ids_find(deck_name)]

    def get_note_ids_find(self, deck_name):
        return self.collection.findNotes("'deck:" + deck_name + "'")

    # Todo:
    # Bad, need to switch to API usage if ever available. As an option - implement them myself.
    def get_card_ids(self, deck_id):
        # We don't use DeckManager.cids(), as we want to export cards in cram decks too.
        return self.collection.db.list(
            "SELECT id FROM cards WHERE did=? OR odid=?", deck_id, deck_id)

    def get_notes_from_cards(self, card_ids):
        card_ids_str = anki.utils.ids2str(card_ids)
        return set(self.collection.db.list("SELECT nid FROM cards WHERE id IN " + card_ids_str))

    def get_note_ids(self, deck_name):
        deck_id = self.collection.decks.byName(deck_name)["id"]
        card_ids = self.get_card_ids(deck_id)
        return self.get_notes_from_cards(card_ids)

    def process_dependencies(self):
        pass


class JsonSerializable(object):
    readable_names = {}
    filter_set = set()

    @staticmethod
    def default_json(wobject):
        if isinstance(wobject, JsonSerializable):
            return wobject.flatten()

        raise TypeError

    def flatten(self):
        return {self.readable_names[key] if key in self.readable_names else key: value
                for key, value in merge_dicts(self.__dict__, self._dict_extension()).iteritems() if
                key not in self.filter_set}

    def _dict_extension(self):
        return {}


class Deck(JsonSerializable):
    filter_set = {"anki_deck", "collection"}

    def __init__(self):
        self.collection = None
        self.name = None
        self.anki_deck = None
        self.notes = None
        self.children = None

    @classmethod
    def from_collection(cls, collection, name):
        deck = Deck()
        deck.collection = collection
        deck.name = name

        deck.update_db()
        deck.anki_deck = collection.decks.byName(name)

        deck.notes = Note.get_notes_from_collection(collection, deck.anki_deck["id"])  # Todo ugly

        deck.children = [cls.from_collection(collection, child_name) for child_name, _ in
                         collection.decks.children(deck.anki_deck["id"])]

        return deck

    def update_db(self):
        # Introduce uuid field for unique identification of entities
        db_util.add_column(self.collection.db, "notes", UUID_FIELD_NAME)

    def _dict_extension(self):
        return self.anki_deck


class Note(JsonSerializable):
    filter_set = {"anki_note", "col"}

    def __init__(self):
        self.anki_note = None

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
        note.anki_note = AnkiNote(collection, id=note_id)
        return note

    def _dict_extension(self):
        return self.anki_note.__dict__


class NoteModel(object):
    def __init__(self):
        pass

    def from_collection(self, collection, model_id):
        self.anki_model = collection.models.get(model_id)


class DeckConfig(object):
    def __init__(self):
        pass

    def from_collection(self, collection, deck_config_id):
        self.anki_deck_config = collection.decks.getConf(deck_config_id)


def main():
    deck_name = "tdeckl1"
    collection = Collection(COLLECTION_PATH)
    # tw = JsonExporter(collection)
    deck = Deck.from_collection(collection, deck_name)

    result_filename = "../result.json"
    print(os.path.realpath(os.path.curdir))

    with open(result_filename, mode='w') as result_file:
        result_file.write(json.dumps(deck, default=Deck.default_json, sort_keys=True, indent=4))

    pprint((json.dumps(deck, default=Deck.default_json, sort_keys=True, indent=4)))


if __name__ == "__main__":
    main()

# Todo trigger backup before export/import.
# Need backup for export because plan to alter table to add uuid

# Todo collection close when outside of anki
# Todo commandline parameters for collection/deck/etc

# Todo for media - store in directory hierarchy corresponding to deck/subdeck hierarchy

# Todo - generate new uuid if :
# Store entity without one
# Load entity without one

# Generate error if trying to load several entities with same uuid
# What if I have cards with same UIID but in different deck? {
# I would think I should treat this kind of situation as a move?
# Also consider - change structure of sub-decks}

# Todo define definite order of save/load

"""
Info:
AnkiNote.mod - modification time
AnkiNote.mid - model id


Warning:
Creation of collection has a side effect of changing current directory to ${collection_path}/collection.media
"""
