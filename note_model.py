class NoteModel(object):
    def __init__(self):
        pass

    def from_collection(self, collection, model_id):
        self.anki_model = collection.models.get(model_id)