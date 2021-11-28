from collections import namedtuple, defaultdict
from typing import Callable, Any, Iterable

from .deck_config import DeckConfig
from .json_serializable import JsonSerializableAnkiDict
from .note_model import NoteModel
from ..anki.adapters.file_provider import FileProvider
from ..importer.import_dialog import ImportConfig
from ..utils import utils
from ..utils.constants import UUID_FIELD_NAME
from ..utils.uuid import UuidFetcher
from ..utils.notifier import AnkiModalNotifier

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
                         "notes",
                         "deck_config_uuid"}

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

        # TODO Remove this once enough time has passed that #106/#116
        # is no longer an issue — i.e. when there are likely no more
        # Anki dbs with a `deck_config_uuid` attached to the deck.
        # See #133.
        if "deck_config_uuid" in self.anki_dict:
            del self.anki_dict["deck_config_uuid"]

        self.metadata.deck_configs.setdefault(new_config.get_uuid(), new_config)

    def serialization_dict(self):
        return utils.merge_dicts(
            super(Deck, self).serialization_dict(),
            {"media_files": list(sorted(self.get_media_file_list(include_children=False)))},
            {"note_models": list(self.metadata.models.values()),
             "deck_configurations": list(self.metadata.deck_configs.values())} if not self.is_child else {})

    def get_media_file_list(self, data_from_models=True, include_children=True):
        media = set()
        for note in self.notes:
            anki_object = note.anki_object
            # TODO Remove compatibility shims for Anki 2.1.46 and
            # lower.
            join_fields = anki_object.joined_fields if hasattr(anki_object, 'joined_fields') else anki_object.joinedFields
            for media_file in self.collection.media.filesInStr(anki_object.mid, join_fields()):
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

    def save_to_collection(self, collection, import_config: ImportConfig):
        self.save_metadata(collection)

        self.save_decks_and_notes(collection=collection,
                                  parent_name="",
                                  model_map_cache=defaultdict(dict),
                                  import_config=import_config)

    def save_metadata(self, collection):
        for config in self.metadata.deck_configs.values():
            config.save_to_collection(collection)

        for note_model in self.metadata.models.values():
            note_model.save_to_collection(collection)

    def save_decks_and_notes(self, collection, parent_name, model_map_cache, import_config: ImportConfig):
        full_name = self._save_deck(collection, parent_name)

        for child in self.children:
            child.save_decks_and_notes(collection=collection,
                                       parent_name=full_name,
                                       model_map_cache=model_map_cache,
                                       import_config=import_config)

        if import_config.use_notes:
            for note in self.notes:
                note.save_to_collection(collection, self, model_map_cache, import_config=import_config)

    def _save_deck(self, collection, parent_name):
        full_name = (parent_name + self.DECK_NAME_DELIMITER if parent_name else "") + self.anki_dict["name"]

        deck_dict = UuidFetcher(collection).get_deck(self.get_uuid())

        deck_id = collection.decks.id(full_name, create=False)
        if deck_id and (not deck_dict or deck_dict["id"] != deck_id):
            full_name = self._rename_deck(full_name, collection)

        if not deck_dict:
            new_deck_id = collection.decks.id(full_name)
            deck_dict = collection.decks.get(new_deck_id)

        deck_dict.update(self.anki_dict)

        self.anki_dict = deck_dict
        self.anki_dict["name"] = full_name

        try:
            self.anki_dict["conf"] = self.metadata.deck_configs[self.deck_config_uuid].anki_dict["id"]
            # TODO Remove the exception-handling once we're confident
            # that there are no more buggy decks, with mismatching
            # `deck_config_uuid`s.
            # See #133.
        except KeyError as error:
            AnkiModalNotifier().error("Incorrect deck config",
                                      "The deck config uuid {} is not present in the deck. "
                                      "This is likely due to a now-fixed bug in CrowdAnki. "
                                      "Please ask the maintainer of the deck to re-export it, if possible. "
                                      "See here: https://github.com/Stvad/CrowdAnki/issues/106 "
                                      "for details and alternative solutions.".format(error))
            raise

        collection.decks.save(deck_dict)

        return full_name

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
