import json
from collections import namedtuple

from anki.exporting import AnkiExporter

import CrowdAnki.utils
from CrowdAnki import utils
from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.deck_config import DeckConfig
from CrowdAnki.json_serializable import JsonSerializableAnkiDict
from CrowdAnki.note import Note
from CrowdAnki.note_model import NoteModel


class Deck(JsonSerializableAnkiDict):
    Metadata = namedtuple("DeckMetadata", ["deck_configs", "models"])
    # Todo either unpack or represent differently because right now - not serialized properly

    filter_set = JsonSerializableAnkiDict.filter_set | \
                 {"collection",
                  "newToday",
                  "revToday",
                  "timeToday",
                  "lrnToday",
                  "metadata",
                  "browserCollapsed",
                  "collapsed"}

    # todo super(Deck, self)

    def __init__(self, anki_deck=None, is_child=False):
        super(Deck, self).__init__(anki_deck)
        self.is_child = is_child

        self.collection = None
        # self.name = None
        self.notes = None
        self.children = None
        self.metadata = None
        self.deck_config_uuid = None

    @classmethod
    def from_collection(cls, collection, name, deck_metadata=None, is_child=False):
        deck = Deck()

        # deck._update_db()
        anki_dict = collection.decks.byName(name)

        deck = Deck(anki_dict, is_child)

        deck.collection = collection
        # deck.name = name

        deck._update_fields()

        deck.metadata = deck_metadata
        deck._load_metadata()

        deck.notes = Note.get_notes_from_collection(collection, deck.anki_dict["id"], deck.metadata.models)

        deck.children = [cls.from_collection(collection, child_name, deck_metadata, True) for child_name, _ in
                         collection.decks.children(deck.anki_dict["id"])]

        return deck

    def _update_db(self):
        # Introduce uuid field for unique identification of entities
        CrowdAnki.utils.add_column(self.collection.db, "notes", UUID_FIELD_NAME)

    def _load_metadata(self):
        if not self.metadata:
            self.metadata = Deck.Metadata({}, {})

        self._load_deck_config()

    def _load_deck_config(self):
        # Todo switch to uuid
        new_config = DeckConfig.from_collection(self.collection, self.anki_dict["conf"])
        self.deck_config_uuid = new_config.get_uuid()

        self.metadata.deck_configs.setdefault(new_config.get_uuid(), new_config)

    def serialization_dict(self):
        return utils.merge_dicts(
            super(Deck, self).serialization_dict(),
            {"media_files": list(self.get_media_file_list(include_children=False))},
            {"note_models": self.metadata.models.values(),
             "deck_configurations": self.metadata.deck_configs.values()} if not self.is_child else {})

    def get_media_file_list(self, data_from_models=True, include_children=True):
        media = set()
        for note in self.notes:
            for media_file in self.collection.media.filesInStr(note.anki_object.mid, note.anki_object.joinedFields()):
                media.add(media_file)

        if include_children:
            for child in self.children:
                media |= child.get_media_file_list(False, include_children)

        return media | (self._get_media_from_models() if data_from_models else set())

    def _get_media_from_models(self):
        anki_exporter = AnkiExporter(self.collection)
        model_ids = [model.anki_dict["id"] for model in self.metadata.models.values()]

        return anki_exporter.get_files_for_models(model_ids, self.collection.media.dir())

    def _load_metadata_from_json(self, json_dict):
        if not self.metadata:
            self.metadata = self.Metadata({}, {})

        # Todo get_uuid?
        new_models = utils.merge_dicts(self.metadata.models,
                                       {model[UUID_FIELD_NAME]: NoteModel.from_json(model) for model in
                                        json_dict.get("note_models", [])})

        new_deck_configs = utils.merge_dicts(self.metadata.deck_configs,
                                             {deck_config[UUID_FIELD_NAME]: DeckConfig.from_json(deck_config) for
                                              deck_config in
                                              json_dict["deck_configurations"]})

        self.metadata = Deck.Metadata(new_deck_configs, new_models)

    @classmethod
    def from_json(cls, json_dict, deck_metadata=None):
        """load metadata, load notes, load children"""
        # todo filter some  parts
        deck = Deck(json_dict)
        deck.metadata = deck_metadata

        if not deck.metadata:  # Todo mental check. The idea is that children don't have metadata
            deck._load_metadata_from_json(json_dict)

        deck.notes = [Note.from_json(json_note) for json_note in json_dict["notes"]]

        deck.children = [cls.from_json(child, deck.metadata) for child in json_dict["children"]]

        return deck

    def save_to_collection(self, collection):
        for config in self.metadata.deck_configs.values():
            config.save_to_collection(collection)

        for note_model in self.metadata.models.values():
            note_model.save_to_collection(collection)

        # Todo renaming on name match - right now - override
        # Todo get deck config by uuid, right now - match on old id
        # Todo uuid

        deck_id = collection.decks.id(self.anki_dict["name"])

        in_dict = collection.decks.get(deck_id)
        in_dict.update(self.anki_dict)
        in_dict["id"] = deck_id
        self.anki_dict = in_dict

        collection.decks.save()
        collection.decks.flush()

        for child in self.children:
            child.save_to_collection(collection)

        for note in self.notes:
            note.save_to_collection(collection, self.metadata.models)