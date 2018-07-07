from collections import namedtuple

from ..anki_overrides.change_model_dialog import ChangeModelDialog

from ..utils import utils
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

    @staticmethod
    def check_semantically_identical(first_model, second_model):
        field_names = ("flds", "tmpls")
        for field in field_names:
            if not utils.json_compare(first_model.anki_dict[field], second_model.anki_dict[field]):
                return False

        return True

    def save_to_collection(self, collection):
        # Todo regenerate cards on update
        # look into template manipulation in "models"

        note_model_dict = collection.models.get_by_uuid(self.get_uuid()) or \
                          collection.models.new(self.anki_dict["name"])

        new_model = note_model_dict["id"] is None

        self.anki_dict = utils.merge_dicts(note_model_dict, self.anki_dict)
        if new_model:
            collection.models.add(self.anki_dict)
        else:
            collection.models.update(self.anki_dict)
        collection.models.flush()

        if not new_model:
            self.update_cards(collection, note_model_dict)

    def make_current(self, collection):
        # Sync through setting global "current" model makes me sad too, but it's ingrained on many levels down
        collection.models.setCurrent(self.anki_dict)
        collection.decks.current()['mid'] = self.anki_dict["id"]

    def update_cards(self, collection, old_model):
        if self.check_semantically_identical(NoteModel.from_json(old_model), self):
            return

        self.make_current(collection)

        old_model["name"] += " *old"

        # todo: check if we are in "ui mode"
        # todo: handle canceled
        # todo: think on "mixed update" handling

        # todo signals instead of direct dialog creation?

        ChangeModelDialog(collection, collection.models.nids(old_model), old_model).exec_()
