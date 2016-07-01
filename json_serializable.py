from uuid import uuid1

from CrowdAnki import utils
from CrowdAnki.common_constants import UUID_FIELD_NAME
from CrowdAnki.utils import merge_dicts


class JsonSerializable(object):
    readable_names = {}
    filter_set = {"mod",  # Modification time
                  "usn"  # Todo clarify
                  }

    def __init__(self):
        pass
        # self._update_fields()

    @staticmethod
    def default_json(wobject):
        if isinstance(wobject, JsonSerializable):
            return wobject.flatten()

        raise TypeError

    @staticmethod
    def json_object_hook(json_dict):
        # Add names to locals()
        from CrowdAnki.deck import Deck
        from CrowdAnki.deck_config import DeckConfig
        from CrowdAnki.note import Note
        from CrowdAnki.note_model import NoteModel

        object_type = json_dict.get("__type__", "")
        type_class = locals().get(object_type, None)
        if type_class:
            return type_class.from_json(json_dict)

        return json_dict

    @classmethod
    def from_collection(cls, collection, entity_id):
        """
        Initializes object from Anki collection
        :param collection:
        :param entity_id:
        :return:
        """

    @classmethod
    def from_json(cls, json_dict):
        """
        Initialize object from json dictionary
        :param json_dict:
        :return:
        """

    def flatten(self):
        return {self.readable_names[key] if key in self.readable_names else key: value
                for key, value in self.serialization_dict().items() if
                key not in self.filter_set}

    def serialization_dict(self):
        return merge_dicts(self.__dict__,
                           {"__type__": self.__class__.__name__})

    def _update_fields(self):
        """
        Add necessary fields to anki dicts/objects. E.g. uuid
        """

    def get_uuid(self):
        self._update_fields()
        # Todo consider introducing this in another way
        """
        :return: Unique identificator in a string format.
        """

    def save_to_collection(self, collection):
        """
        Save content to anki collection
        :param collection:
        :return:
        """


class JsonSerializableAnkiDict(JsonSerializable):
    filter_set = JsonSerializable.filter_set | {"anki_dict"}

    def __init__(self, anki_dict=None):
        super(JsonSerializableAnkiDict, self).__init__()
        self.anki_dict = anki_dict

    def serialization_dict(self):
        return utils.merge_dicts(super(JsonSerializableAnkiDict, self).serialization_dict(),
                                 self.anki_dict)

    def _update_fields(self):
        self.anki_dict.setdefault(UUID_FIELD_NAME, str(uuid1()))

    def get_uuid(self):
        super(JsonSerializableAnkiDict, self).get_uuid()
        return self.anki_dict[UUID_FIELD_NAME]

    @classmethod
    def from_json(cls, json_dict):
        anki_dict_object = cls(json_dict)
        del anki_dict_object.anki_dict["__type__"]
        return anki_dict_object


class JsonSerializableAnkiObject(JsonSerializable):
    filter_set = JsonSerializable.filter_set | {"anki_object", "anki_object_dict"}

    def __init__(self, anki_object=None):
        super(JsonSerializableAnkiObject, self).__init__()
        self.anki_object = anki_object
        self.anki_object_dict = getattr(anki_object, "__dict__", None)

    def serialization_dict(self):
        return utils.merge_dicts(super(JsonSerializableAnkiObject, self).serialization_dict(),
                                 self.anki_object.__dict__)

    def _update_fields(self):
        utils.add_absent_field(self.anki_object, UUID_FIELD_NAME, str(uuid1()))

    def get_uuid(self):
        super(JsonSerializableAnkiObject, self).get_uuid()
        return getattr(self.anki_object, UUID_FIELD_NAME)
