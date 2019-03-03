from collections import namedtuple, defaultdict

from typing import Callable, Any, Iterable

from .deck_config import DeckConfig
from .json_serializable import JsonSerializableAnkiDict
from .note_model import NoteModel
from ..anki.adapters.file_provider import FileProvider
from ..utils import utils
from ..utils.constants import UUID_FIELD_NAME

DeckMetadata = namedtuple("DeckMetadata", ["deck_configs", "models"])


class Deck(JsonSerializableAnkiDict):
    DECK_NAME_DELIMITER = "::"

    export_filter_set = JsonSerializableAnkiDict.export_filter_set | \
                        {
                            "collection",  # runtime-relevant
                            "newToday",
                            "revToday",
                            "timeToday",
                            "lrnToday",
                            "metadata",
                            "browserCollapsed",
                            "collapsed",
                            "is_child",  # runtime-relevant
                            "conf",  # uuid
                            "file_provider_supplier"
                        }

    import_filter_set = JsonSerializableAnkiDict.import_filter_set | \
                        {"note_models",
                         "deck_configurations",
                         "children",
                         "media_files",
                         "notes"}

    def __init__(self,
                 file_provider_supplier: Callable[[Any, Iterable[int]], FileProvider],
                 anki_deck=None,
                 is_child=False):
        super().__init__(anki_deck)

        self.file_provider_supplier = file_provider_supplier
        self.is_child = is_child

        self.collection = None
        self.notes = []
        self.children = []
        self.metadata = None
        self.deck_config_uuid = None

    def flatten(self):
        """
        Specification in order to store only deck lowest level name in JSON
        :return:
        """
        result = super(Deck, self).flatten()
        if self.is_child:
            result["name"] = result["name"].split(self.DECK_NAME_DELIMITER)[-1]

        return result

    def get_note_count(self):
        return len(self.notes) + sum(child.get_note_count() for child in self.children)

    def _update_db(self):
        # Introduce uuid field for unique identification of entities
        utils.add_column(self.collection.db, "notes", UUID_FIELD_NAME)

    def _load_metadata(self):
        if not self.metadata:
            self.metadata = DeckMetadata({}, {})

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
            {"note_models": list(self.metadata.models.values()),
             "deck_configurations": list(self.metadata.deck_configs.values())} if not self.is_child else {})

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
        model_ids = [model.anki_dict["id"] for model in self.metadata.models.values()]
        file_provider = self.file_provider_supplier(self.collection, model_ids)

        return file_provider.get_files()

    def _load_metadata_from_json(self, json_dict):
        if not self.metadata:
            self.metadata = DeckMetadata({}, {})

        note_models_list = [NoteModel.from_json(model) for model in json_dict.get("note_models", [])]
        new_models = utils.merge_dicts(self.metadata.models,
                                       {model.get_uuid(): model for model in note_models_list})

        deck_config_list = [DeckConfig.from_json(deck_config) for deck_config in
                            json_dict.get("deck_configurations", [])]

        new_deck_configs = utils.merge_dicts(self.metadata.deck_configs,
                                             {deck_config.get_uuid(): deck_config for deck_config in deck_config_list})

        self.metadata = DeckMetadata(new_deck_configs, new_models)

    def save_to_collection(self,
                           collection,
                           parent_name="",
                           save_configs=True,
                           save_note_models=True,
                           model_map_cache=None):
        if save_configs:  # Todo when update implemented multiple save can be harmless and code simpler
            for config in self.metadata.deck_configs.values():
                config.save_to_collection(collection)

        if save_note_models:
            for note_model in self.metadata.models.values():
                note_model.save_to_collection(collection)

        name = self._save_deck(collection, parent_name)

        model_map_cache = model_map_cache or defaultdict(dict)
        for child in self.children:
            child.save_to_collection(collection,
                                     parent_name=name,
                                     save_configs=False,
                                     save_note_models=False,
                                     model_map_cache=model_map_cache)

        for note in self.notes:
            note.save_to_collection(collection, self, model_map_cache)

    def _save_deck(self, collection, parent_name):
        name = (parent_name + self.DECK_NAME_DELIMITER if parent_name else "") + self.anki_dict["name"]

        deck_dict = collection.decks.get_deck_by_uuid(self.get_uuid())

        deck_id = collection.decks.id(name, create=False)
        if deck_id and (not deck_dict or deck_dict["id"] != deck_id):
            name = self._rename_deck(name, collection)

        if not deck_dict:
            new_deck_id = collection.decks.id(name)
            deck_dict = collection.decks.get(new_deck_id)

        deck_dict.update(self.anki_dict)

        self.anki_dict = deck_dict
        self.anki_dict["name"] = name
        self.anki_dict["conf"] = self.metadata.deck_configs[self.deck_config_uuid].anki_dict["id"]
        collection.decks.save()
        collection.decks.flush()

        return name

    @staticmethod
    def _rename_deck(initial_name, collection):
        """Adds unique suffix to the name, until it becomes unique (required by Anki)"""
        # Todo consider popup

        # This approach can be costly if we have a lot of decks with specific set of names.
        # And adding random appendix would've been faster, but less user-friendly
        number = 2
        deck_id = collection.decks.id(initial_name, create=False)
        new_name = ""
        while deck_id:
            new_name = initial_name + "_" + str(number)
            number += 1
            deck_id = collection.decks.id(new_name, create=False)

        return new_name
