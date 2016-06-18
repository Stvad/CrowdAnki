import json
import anki
from pprint import pprint

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import QAction, SIGNAL

from anki import Collection

COLLECTION_PATH="../../WCollection/collection.anki2"

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
    def __init__(self, collection): # Todo default parameter current running collection
        self.collection = collection

        # for deck in self.collection.decks.all():
        #     pprint(deck)

        deckname = "VideoStitch Insights"

        # for note in self.collection.findNotes('"deck:Software::Bash::Shell navigation"'):
        #     pprint(note)

        pprint(self.get_note_ids(deckname))
        pprint(self.get_note_ids_find(deckname))

    def export_deck(self, deck_id):
        """Returns json for given deck and list of dependencies"""
        working_deck = self.collection.decks.get(deck_id)

        for child in working_deck.children():
            pass

    def get_notes(self, deck_id):
        pass

    def get_note_ids_find(self, deck_name):
        return self.collection.findNotes("'deck:" + deck_name + "'")

    # Todo:
    # Bad, need to switch to API usage if ever available. As an option - implement them myself.
    def get_card_ids(self, deck_id):
        # We don't use DeckManager.cids(), as we want to export cards in cram decks too.
        return self.collection.db.list(
            "select id from cards where did=? or odid=?", deck_id, deck_id)

    def get_notes_from_cards(self, card_ids):
        card_ids_str = anki.utils.ids2str(card_ids)
        return set(self.collection.db.list("select nid from cards where id in " + card_ids_str))

    def get_note_ids(self, deck_name):
        deck_id = self.collection.decks.byName(deck_name)["id"]
        card_ids = self.get_card_ids(deck_id)
        return self.get_notes_from_cards(card_ids)

    def process_dependencies(self):
        pass


def main():
    collection = Collection(COLLECTION_PATH)
    tw = JsonExporter(collection)

    pprint(tw)

if __name__ == "__main__":
    main()