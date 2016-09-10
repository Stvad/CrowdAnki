# CrowdAnki

**CrowdAnki** is a plugin for http://ankisrs.net/ that allows users to import and export decks/notes and all relevant information in a hierarchical JSON format. The main purpose is to facilitate crowdsourcing for Anki decks and notes.

AnkiWeb link for the plugin (may not contain the latest version): https://ankiweb.net/shared/info/1788670778?ok=1

## Suggested collaboration workflow
The current workflow could be described as following:
* The user creates or imports a deck inside of Anki.
* Makes some modification to it (i.e. to notes, deck settings, deck structure or note models).
* Then the user can export the deck in JSON format (accompanied by media directory with media files used in that deck) and share it with other users. For example by creating Github repo with it.
* Other people then can either modify JSON directly or import the deck to their instance of Anki and then make some modifications to it.
* Original JSON then can be updated the with the changes, these people made (merging several changes together if necessary).
* After that original user (and other people) can import updated deck to integrate these new changes into their collection.


## Export
To perform the export go to menu File>Export

Select the deck (**note**: export of "All decks" is not supported, you need to select a specific deck) and the export format "CrowdAnki JSON representation".
After pressing the Export button - select directory where the result should be stored.

## Import
To perform the import go to menu File>"Import CrowdAnki Json" and select the directory where the deck is stored.

### Things to note for the Import:
* Automatic backup would be triggered prior to the import;
* If note model for the note has changed, or if note model itself changed in a way that it's not easy to update it automatically: you would be prompted with the window, that will ask you to specify correspondence between old and new model;
* If the note was moved to another deck in JSON file, on import all cards from that note (except the ones, that are in dynamic decks) will be moved to the specified deck.

## Other

This plugin works with [AnkiHub plugin](https://ankiweb.net/shared/info/116826216) ([Github](https://github.com/dayjaby/AnkiHub)) to provide you better plugin management experience. 

With AnkiHub you can install plugins directly from Github and receive updates automatically.

