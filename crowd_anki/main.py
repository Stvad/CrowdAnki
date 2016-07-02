import os.path

from anki_importer import AnkiJsonImporter
from anki_exporter import AnkiJsonExporter
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library

from anki import Collection

COLLECTION_PATH = "../../WCollection/collection.anki2"


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


def main():
    deck_name = "tdeckl1"
    collection = Collection(COLLECTION_PATH)
    print(os.path.realpath(os.path.curdir))

    exporter = AnkiJsonExporter(collection)
    exporter.export_deck(deck_name)

    deck_directory = os.path.join("./", deck_name)
    deck_json = os.path.join(deck_directory, deck_name + ".json")

    importer = AnkiJsonImporter(collection)
    importer.load_from_file(deck_json)

    # deck.notes[0].anki_object.flush(mod=True)
    collection.close()

def anki_init():
    pass


if __name__ == "__main__":
    main()
else:
    anki_init()

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
