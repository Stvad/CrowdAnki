from crowd_anki.utils import utils

from json_serializable import JsonSerializableAnkiDict


class NoteModel(JsonSerializableAnkiDict):
    export_filter_set = JsonSerializableAnkiDict.export_filter_set | {"did"}

    def __init__(self, anki_model=None):
        super(NoteModel, self).__init__(anki_model)

    @classmethod
    def from_collection(cls, collection, model_id):
        anki_dict = collection.models.get(model_id)
        note_model = NoteModel(anki_dict)
        note_model._update_fields()

        return note_model

    def save_to_collection(self, collection):
        # Todo regenerate cards on update
        # look into template manipulation in "models"

        note_model_dict = collection.models.get_by_uuid(self.get_uuid()) or \
                          collection.models.new(self.anki_dict["name"])

        self.anki_dict = utils.merge_dicts(note_model_dict, self.anki_dict)
        collection.models.update(self.anki_dict)
        collection.models.flush()
