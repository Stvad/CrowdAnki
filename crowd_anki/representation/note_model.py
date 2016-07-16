from collections import namedtuple

from aqt.dialog.change_model import ChangeModelDialog
from crowd_anki.utils import utils

from .json_serializable import JsonSerializableAnkiDict


class NoteModel(JsonSerializableAnkiDict):
    ModelMap = namedtuple("ModelMap", ["field_map", "template_map"])
    export_filter_set = JsonSerializableAnkiDict.export_filter_set | \
                        {"did"  # uuid
                         }

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

        new_model = note_model_dict["id"] is None

        self.anki_dict = utils.merge_dicts(note_model_dict, self.anki_dict)
        collection.models.update(self.anki_dict)
        collection.models.flush()

        return self.update_cards(collection, note_model_dict) if not new_model else {}

    def update_cards(self, collection, old_model):
        field_names = ("flds", "tmpls")

        for field in field_names:
            if not utils.json_compare(old_model[field], self.anki_dict[field]):
                break
        else:
            return {}

        # Sync through setting global "current" model makes me sad too, but it's ingrained on many levels down
        collection.models.setCurrent(self.anki_dict)
        collection.decks.current()['mid'] = self.anki_dict["id"]

        # todo: check if we are in "ui mode"
        # todo: handle canceled
        dialog = ChangeModelDialog(collection, collection.models.nids(old_model), old_model, self.anki_dict)

        return {self.get_uuid(): NoteModel.ModelMap(dialog.get_field_map(), dialog.get_template_map())}

