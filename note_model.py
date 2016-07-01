from CrowdAnki import utils
from CrowdAnki.json_serializable import JsonSerializableAnkiDict


class NoteModel(JsonSerializableAnkiDict):
    def __init__(self, anki_model=None):
        super(NoteModel, self).__init__(anki_model)

    @classmethod
    def from_collection(cls, collection, model_id):
        anki_dict = collection.models.get(model_id)
        note_model = NoteModel(anki_dict)
        note_model._update_fields()

        return note_model

    def save_to_collection(self, collection):
        default_note_config = collection.models.new(self.anki_dict["name"])
        self.anki_dict = utils.merge_dicts(default_note_config, self.anki_dict)
        collection.models.add(self.anki_dict)
        collection.models.flush()